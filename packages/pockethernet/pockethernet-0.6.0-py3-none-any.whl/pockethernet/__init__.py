import socket
import struct
import time
import pockethernet.crc16
from cobs import cobs
import logging

from scapy.layers.dhcp import BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, LLC, SNAP
from scapy.contrib.cdp import CDPv2_HDR
from scapy.contrib.lldp import LLDPDU

from pockethernet.testresult import WiremapResult, PoEResult, LinkResult, TdrResult, BerResult, DhcpResult, CdpResult, \
    TdrPlotResult

COMMAND_WIREMAP = 48
COMMAND_DEVICEINFO = 1
COMMAND_TDR = 50
COMMAND_PHYCONFIG = 51
COMMAND_TDR_GRAPH = 65
COMMAND_POE = 49
COMMAND_LINK = 52
COMMAND_DHCP = 56
COMMAND_CAPTURE = 53
COMMAND_VLAN = 57
COMMAND_BER = 64
RESULT_WIREMAP = 4144
RESULT_DEVICEINFO = 4097
RESULT_TDR = 4146
RESULT_TDR_GRAPH = 4161
RESULT_POE = 4145
RESULT_LINK = 4099
RESULT_LLDP = 4352
RESULT_ACK = 47806
RESULT_NACK = 51966
RESULT_BER = 4160
PACKET_DHCP = 4353
PACKET_CDPLLDP = 4352
PACKET_TRAFFIC = 4354

PHY_UP = 1
PHY_ISOLATE = 2
PHY_NEGOTIATE_MDI = 4
PHY_NEGOTIATE_MDIX = 8
PHY_NEGOTIATE_ANY = 4 + 8
PHY_DTE_DETECT = 16
PHY_AN_ADV = 32
PHY_ADVERTIZE_10BASET = 64
PHY_ADVERTIZE_100BASET = 128
PHY_ADVERTIZE_1000BASET = 256
PHY_ADVERTIZE_ANY = 64 + 128 + 256
PHY_DUPLEX_HALF = 512
PHY_DUPLEX_FULL = 1024
PHY_DUPLEX_ANY = 512 + 1024
PHY_SELF = 2048
PHY_DOWNSHIFT = 4096


class Pockethernet:

    def __init__(self):
        self.sock = None
        self.lastData = {}
        self.mac = None

    def connect(self, mac, max_tries=None):
        """ Connect to a pockethernet device over bluetooth.

        The pockethernet device has to be bound already using something like the bluetooth dialog in gnome

        :param mac: Bluetooth mac address of the pockethernet
        :param max_tries: Max tries to connect, each try is 1-2 seconds
        :return: True if the connection is successful
        """
        self.mac = mac
        tries = 0
        logging.debug('Connecting to {}'.format(mac))

        # Pockethernet seems to use RFCOMM channel 5
        while True:
            try:
                self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                self.sock.bind((socket.BDADDR_ANY, 0))
                self.sock.connect((mac, 5))
                logging.debug('Connection to {} successful'.format(mac))
                return True
            except OSError as e:
                logging.debug(e)
                tries += 1
                if max_tries is not None and tries > max_tries:
                    logging.debug('Max tries exceeded')
                    return False
                time.sleep(1)

    def send_command(self, command, data):
        logging.debug("Sending command {} with {} bytes data".format(command, len(data)))

        # First is command ID, the 0 is reserved space for a checksum
        header = struct.pack('<HH', command, 0)
        data = struct.pack('<{}s'.format(len(data)), data)
        packet = header + data

        # Calculate the checksum and pack the header again with it
        crc = pockethernet.crc16.crc16xmodem(packet, -1)
        header = struct.pack('<HH', command, crc)
        packet = header + data

        # Run COBS encoding on the data and add null bytes for framing
        encoded = cobs.encode(packet)
        raw = b'\0' + encoded + b'\0'

        # Hope that the pockethernet enjoys this packet
        self.sock.send(raw)

    def read_packet(self, until=None):
        if until is None:
            logging.debug('Reading any packet')
        elif until == RESULT_ACK or until == RESULT_NACK:
            pass
        else:
            logging.debug('Reading a packet (waiting for {})'.format(until))
        while True:
            raw = self.sock.recv(1024)
            while raw[-1:] != b'\0':
                raw += self.sock.recv(1024)
            packets = raw.split(b'\0')
            packets = list(filter(None, packets))
            for packet in packets:
                packet = cobs.decode(packet)
                header = struct.unpack_from('<HH', packet)
                data = struct.unpack_from('<{}s'.format(len(packet) - 4), packet, 4)
                packet_type = header[0]

                if packet_type == RESULT_ACK:
                    logging.debug('Got ACK')
                    return
                elif packet_type == RESULT_NACK:
                    raise ValueError("Got NACK from pockethernet")

                self.lastData[packet_type] = data[0]
                logging.debug('Got packet with type {} and length {}'.format(packet_type, len(data[0])))
                if (isinstance(until, int) and packet_type == until) or (
                        isinstance(until, list) and packet_type in until):
                    if isinstance(until, list):
                        return packet_type, data[0]
                    else:
                        return data[0]
                else:
                    logging.warn('Got unexpected packet {} size {}'.format(packet_type, len(data[0])))

    def get_device_info(self):
        self.send_command(COMMAND_DEVICEINFO, b'')
        result = self.read_packet(RESULT_DEVICEINFO)
        result = struct.unpack_from('<BBBBBB', result)
        mac = '28:FD:80:{:02X}:{:02X}:{:02X}'.format(result[2], result[1], result[0])
        return {
            'hardware': result[4],
            'firmware': result[5],
            'mac': mac
        }

    def get_wiremap(self):
        self.send_command(COMMAND_WIREMAP, b'')
        result = self.read_packet(RESULT_WIREMAP)
        return WiremapResult(result)

    def get_poe(self):
        config = struct.pack('<HH', 3000, 100)
        self.send_command(COMMAND_POE, config)
        result = self.read_packet(RESULT_POE)
        return PoEResult(result)

    def _make_marvell_link_bitfield(self, speed=PHY_ADVERTIZE_ANY, duplexity=PHY_DUPLEX_ANY,
                                    negotiate=PHY_NEGOTIATE_ANY, up=True):
        if up:
            return PHY_UP + PHY_ISOLATE + PHY_AN_ADV + speed + duplexity + negotiate
        else:
            return PHY_ISOLATE

    def get_link(self, speed=PHY_ADVERTIZE_ANY):
        phy = self._make_marvell_link_bitfield(speed=speed)
        config = struct.pack('<IH', phy, 8000)
        self.send_command(COMMAND_LINK, config)
        result = self.read_packet(RESULT_LINK)

        return LinkResult(result)

    def link_reset(self):
        logging.info('Reset link')
        phy = self._make_marvell_link_bitfield(up=False)
        config = struct.pack('<ih', phy, 8000)
        self.send_command(COMMAND_PHYCONFIG, config)
        self.read_packet(RESULT_ACK)

    def enable_dhcp(self):
        logging.info('Enable DHCP')
        self.send_command(COMMAND_DHCP, b'')
        self.read_packet(RESULT_ACK)

    def set_capture_mode(self, dhcp=False, lldp=False, traffic=False):
        flag = 0
        if dhcp:
            flag += 1
        if lldp:
            flag += 2
        if traffic:
            flag += 4
        config = struct.pack('<ii', flag, 0)
        logging.info('Set capture flag to {}'.format(flag))
        self.send_command(COMMAND_CAPTURE, config)
        self.read_packet(RESULT_ACK)

    def set_vlan(self, vid):
        config = struct.pack('<i', vid)
        logging.info('Set vlan to {}'.format(vid))
        self.send_command(COMMAND_VLAN, config)
        self.read_packet(RESULT_ACK)

    def debug(self, send=None):
        if send:
            self.send_command(send, b'')
        self.read_packet()

    def get_tdr(self, long_distance=False):
        short_pulse = not long_distance
        magic = 0
        pulse_length = 3
        if short_pulse:
            pulse_length = 0
            magic = 23

        # More magic
        config = [1, pulse_length, 1, 0, 5, 4, magic, 3, 0, 0, 0, 0, 0, 0, 0]
        config = struct.pack('<BBBBBBBBBBBBBBB', *config)

        self.send_command(COMMAND_TDR, config)
        result = self.read_packet(until=RESULT_TDR)
        return TdrResult(result, long_distance)

    def get_tdr_plot(self, end_distance):
        logging.info('Bring phy up')
        phy = self._make_marvell_link_bitfield(up=True)
        config = struct.pack('<ih', phy, 8000)
        self.send_command(COMMAND_PHYCONFIG, config)
        self.read_packet(RESULT_ACK)

        logging.info('Running tdr plot')
        end_distance_meter = end_distance
        if end_distance > 30:
            magic = 23
            pulse_length = 0
            end_distance = (end_distance + 17.33562) / 0.8058546 + 0.5
        else:
            pulse_length = 3
            magic = 10
            end_distance = (end_distance + 6.1809) / 0.759606 + 0.5

        config = [0, pulse_length, 0, 7, magic, int(end_distance)]
        print(config)
        config = struct.pack('<BBBBHH', *config)
        self.send_command(COMMAND_TDR_GRAPH, config)
        result = self.read_packet(until=RESULT_TDR_GRAPH)
        return TdrPlotResult(result, end_distance, end_distance_meter, magic)

    def get_ber(self, speed=10, large_packet=False, random=True):
        if speed == 10:
            speed = 1
            timeout = 5
        elif speed == 100:
            speed = 2
            timeout = 50
        elif speed == 1000:
            speed = 3
            timeout = 200
        else:
            raise ValueError("speed should be 10, 100 or 1000")

        packet_size = 1
        if large_packet:
            packet_size = 2

        payload = 2
        if random:
            payload = 1

        config = [8000, 2000, speed, packet_size, payload, 200, timeout]
        config = struct.pack('<HHBBBBB', *config)
        self.send_command(COMMAND_BER, config)
        result = self.read_packet(until=RESULT_BER)
        return BerResult(result)

    def wait_for_capture_results(self, timeout=60, wait_for=None):
        if wait_for is None:
            wait_for = [PACKET_DHCP, PACKET_CDPLLDP]
        ptype, result = self.read_packet(until=wait_for)
        if ptype == PACKET_DHCP:
            logging.info('Got DHCP clease')
            ether = Ether(result)
            ether.show()
            ip = IP(ether.payload)
            udp = UDP(ip.payload)
            dhcp = BOOTP(udp.payload)
            return DhcpResult(dhcp)
        elif ptype == PACKET_CDPLLDP:
            logging.info('Got CDP/LLDP packet')
            ether = Ether(result)
            ether.show()
            llc = LLC(ether.payload)
            snap = SNAP(llc.payload)
            if snap.fields['OUI'] == 0xc and snap.fields['code'] == 0x2000:
                # Packet is CDP
                cdp = CDPv2_HDR(snap.payload)
                return CdpResult(cdp)
            else:
                logging.warning("Unknown SNAP packet")
        else:
            print("Got something")
            logging.error("Unexpected packet received: {}".format(ptype))

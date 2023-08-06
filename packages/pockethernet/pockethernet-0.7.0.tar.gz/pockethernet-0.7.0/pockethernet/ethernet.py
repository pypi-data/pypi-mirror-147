import struct
import ipaddress


class EthernetFrame:
    def __init__(self):
        self.source_mac = None
        self.destination_mac = None
        self.ethertype = None


class IPv4Packet:
    def __init__(self):
        self.version = None
        self.ihl = None
        self.dscp = None
        self.ecn = None
        self.length = None
        self.identification = None
        self.flags = None
        self.fragment_offset = None
        self.ttl = None
        self.protocol = None
        self.checksum = None

        self.source_ip = None
        self.destination_ip = None

        self.parent = None


class SnapPacket:
    def __init__(self):
        self.dsap = None
        self.ssap = None
        self.control = None
        self.oui = None
        self.protocol_id = None

        self.parent = None


class UdpPacket:
    def __init__(self):
        self.source_port = None
        self.destination_port = None
        self.length = None
        self.checksum = None

        self.parent = None


class CdpPacket:
    def __init__(self):
        self.version = None
        self.ttl = None
        self.checksum = None

        self.data = []

        self.parent = None

    def describe_data(self):
        result = []
        for type, payload in self.data:
            if type == 0x0001:
                value = payload.decode()
                result.append([type, 'Device ID', value])
            elif type == 0x0002:
                acount, = struct.unpack_from('!I', payload, 0)
                addresses = []
                offset = 4
                for i in range(0, acount):
                    atlv = struct.unpack_from('!BBBH', payload, offset)
                    offset += 2 + atlv[1]
                    addresslength, = struct.unpack_from('!H', payload, offset)
                    offset += 2 + addresslength
                    if atlv[0] == 2:
                        # No parser yet for 802.2 address format
                        addresses.append(payload)
                        continue

                    if atlv[2] != 0xCC:
                        # No parser yet for other protocols than IP
                        addresses.append(payload)
                        continue

                    if atlv[3] == 4:
                        araw, = struct.unpack_from('!I', payload, offset - 4)
                        addresses.append(ipaddress.IPv4Address(araw))
                    elif atlv[3] == 16:
                        araw, = struct.unpack_from('!16s', payload, offset - 16)
                        addresses.append(ipaddress.IPv6Address(araw))
                result.append([type, 'Addresses', addresses])
            elif type == 0x0003:
                value = payload.decode()
                result.append([type, 'Port ID', value])
            elif type == 0x0004:
                caps, = struct.unpack('!I', payload)
                result.append([type, 'Capabilities', caps])
            elif type == 0x0005:
                value = payload.decode()
                result.append([type, 'Software version', value])
            elif type == 0x0006:
                value = payload.decode()
                result.append([type, 'Platform', value])
        return result


class DhcpPacket:
    def __init__(self):
        self.op = None
        self.htype = None
        self.hlen = None
        self.hops = None
        self.xid = None

        self.secs = None
        self.flags = None

        self.ciaddr = None
        self.yiaddr = None
        self.siaddr = None
        self.giaddr = None
        self.chaddr = None
        self.sname = None
        self.file = None
        self.options = []

        self.parent = None

    def describe_options(self):
        result = []
        optnames = {
            1: 'Subnet Mask',
            2: 'Time Offset',
            3: 'Router',
            4: 'Time Server',
            5: 'Name Server',
            6: 'Domain Server',
            7: 'Log Server',
            8: 'Quotes Server',
            9: 'LPR Server',
            10: 'Impress Server',
            11: 'RLP Server',
            12: 'Hostname',
            13: 'Boot File Size',
            14: 'Merit Dump File',
            15: 'Domain Name',
            16: 'Swap Server',
            17: 'Root Path',
            18: 'Extensions Path',
            19: 'IP Forwarding',
            20: 'Non-Local Source Routing',
            21: 'Policy Filter',
            22: 'Maximum Datagram Reassembly Size',
            23: 'Default IP TTL',
            24: 'Path MTU Aging Timeout',
            25: 'Path MTU Plateau Table',
            26: 'Interface MTU',
            27: 'All Subnets are Local',
            28: 'Broadcast Address',
            29: 'Perform Mask Discovery',
            30: 'Mask Supplier',
            31: 'Perform Router Discovery',
            32: 'Router Solicitation Address',
            33: 'Static Route',
            34: 'Trailer Encapsulation',
            35: 'ARP Cache Timeout',
            36: 'Ethernet Encapsulation',
            37: 'TCP Default TTL',
            38: 'TCP Keepalive Interval',
            39: 'TCP Keepalive Garbage',
            40: 'Network Information Service Domain',
            41: 'Network Information Servers',
            42: 'NTP Servers',
            43: 'Vendor Specific Information',
            44: 'NetBIOS over TCP/IP Name Server',
            45: 'NetBIOS over TCP/IP Datagram Distribution Server',
            46: 'NetBIOS over TCP/IP Node Type',
            47: 'NetBIOS over TCP/IP Scope',
            48: 'X Window System Font Server',
            49: 'X Window System Display Manager',
            50: 'Address Request',
            51: 'Address Time',
            52: 'Option Overload',
            53: 'DHCP Message Type',
            54: 'DHCP Server Identification',
            55: 'Parameter Request List',
            56: 'DHCP Message',
            57: 'DHCP Max Message Size',
            58: 'Renewal Time',
            59: 'Rebinding Time',
            60: 'Class Id',
            61: 'Client Id',
            62: 'NetWare/IP Domain',
            63: 'NetWare/IP Option',
            64: 'NIS+ Domain',
            65: 'NIS+ Servers',
            66: 'TFTP Server name',
            67: 'Bootfile name',
            68: 'Mobile IP Home Agent',
            69: 'SMTP Server',
            70: 'POP3 Server',
            71: 'NNTP Server',
            72: 'Default WWW Server',
            73: 'Default Finger Server',
            74: 'Default IRC Server',
            75: 'StreetTalk Server',
            76: 'StreetTalk STDA Server',
        }
        for tag, length, data in self.options:
            if tag in [1, 28, 50, 54]:
                result.append([tag, optnames[tag], ipaddress.IPv4Address(data)])
            elif tag in [3, 4, 5, 6, 7, 8, 9, 10, 11, 41, 42, 44, 45, 48, 49, 65, 68, 69, 70, 71, 73, 74, 75, 76]:
                # Multiple ip addresses decoder
                count = len(data) // 4
                raws = struct.unpack(f'!{count}I', data)
                values = list(map(ipaddress.IPv4Address, raws))
                result.append([tag, optnames[tag], values])
            elif tag in [12, 17, 18, 40, 64, 66, 67]:
                # Null terminated string decoder
                value = struct.unpack(f'!{length}s', data)[0].rstrip(b'\0').decode('ascii')
                result.append([tag, optnames[tag], value])
            elif tag in [19, 20, 27, 29, 30, 31, 34, 36, 39]:
                # Single boolean decoder
                value, = struct.unpack(f'!?', data)
                result.append([tag, optnames[tag], value])
            elif tag in [23, 37, 46, 52]:
                # Single 8 bit int
                value, = struct.unpack(f'!B', data)
                result.append([tag, optnames[tag], value])
            elif tag in [22, 26, 57]:
                # Single 16 bit int
                value, = struct.unpack(f'!H', data)
                result.append([tag, optnames[tag], value])
            elif tag in [35, 38, 51, 58, 59]:
                # Single 32 bit int
                value, = struct.unpack(f'!I', data)
                result.append([tag, optnames[tag], value])
            elif tag == 53:
                value = int(data[0])
                mtype = f'unknown ({value})'
                types = {
                    1: 'Discover',
                    2: 'Offer',
                    3: 'Request',
                    4: 'Decline',
                    5: 'Ack',
                    6: 'Nak',
                    7: 'Release',
                    8: 'Inform',
                }
                if value in types:
                    mtype = types[value]
                result.append([tag, 'DHCP Message Type', mtype])
            elif tag == 51:
                value, = struct.unpack('!I', data)
                result.append([tag, 'Address Lease Time', value])
            elif tag == 33:
                count = len(data) // 8
                raws = struct.unpack(f'!{count * 2}I', data)
                values = list(map(ipaddress.IPv4Address, raws))
                valiter = iter(values)
                routes = []
                for destination in valiter:
                    route = next(valiter)
                    routes.append((destination, route))
                result.append([tag, optnames[tag], routes])
            elif tag == 55:
                count = len(data)
                raws = struct.unpack(f'!{count}B', data)
                result.append([tag, optnames[tag], raws])
        return result


def decode_dhcp(raw, parent=None):
    header = struct.unpack_from('!BBBB I HH IIII 16s 64s 128s 4s', raw, 0)
    data = DhcpPacket()
    data.parent = parent
    data.op = header[0]
    data.htype = header[1]
    data.hlen = header[2]
    data.hops = header[3]
    data.xid = header[4]
    data.secs = header[5]
    data.flags = header[6]

    data.ciaddr = ipaddress.IPv4Address(header[7])
    data.yiaddr = ipaddress.IPv4Address(header[8])
    data.siaddr = ipaddress.IPv4Address(header[9])
    data.giaddr = ipaddress.IPv4Address(header[10])

    data.chaddr = header[11]
    data.sname = header[12].rstrip(b'\0').decode('ascii')
    data.file = header[13].rstrip(b'\0').decode('ascii')
    data.cookie = header[14]

    offset = 240
    while True:
        tag, length = struct.unpack_from('!BB', raw, offset)
        if tag == 255:
            break
        offset += 2
        optiondata, = struct.unpack_from('!{}s'.format(length), raw, offset)
        offset += length
        data.options.append((tag, length, optiondata))
    return data


def decode_udp(raw, parent=None):
    header = struct.unpack_from('!HH HH', raw, 0)
    data = UdpPacket()
    data.source_port = header[0]
    data.destination_port = header[1]
    data.length = header[2]
    data.checksum = header[3]
    data.parent = parent

    if data.source_port == 68 or data.destination_port == 68:
        return decode_dhcp(raw[8:], data)

    return data


def decode_ipv4(raw, parent=None):
    header = struct.unpack_from('!BBH HH BBH II', raw, 0)

    data = IPv4Packet()
    data.version = header[0] >> 4
    data.ihl = header[0] & 0x0F
    data.dscp = header[1] >> 2
    data.ecn = header[1] & 0b00000011
    data.length = header[2]
    data.identification = header[3]
    data.flags = header[4] >> 14
    data.fragment_offset = header[4] & 0b0011111111111111
    data.ttl = header[5]
    data.protocol = header[6]
    data.checksum = header[7]

    data.source_ip = ipaddress.IPv4Address(header[8])
    data.destination_ip = ipaddress.IPv4Address(header[9])

    data.parent = parent

    offset = 4 * data.ihl

    if data.protocol == 17:
        # UDP
        return decode_udp(raw[offset:], data)

    return data


def decode_cdp(raw, parent=None):
    header = struct.unpack_from('!BBH', raw, 0)
    data = CdpPacket()
    data.version = header[0]
    data.ttl = header[1]
    data.checksum = header[2]
    data.parent = parent

    offset = 4
    while offset < len(raw):
        type, length = struct.unpack_from('!HH', raw, offset)
        payload, = struct.unpack_from(f'!{length - 4}s', raw, offset + 4)
        data.data.append([type, payload])
        offset += length

    return data


def decode_snap(raw, parent=None):
    header = struct.unpack_from('!BBB 3s H', raw, 0)
    if header[0] != 0xAA or header[1] != 0xAA:
        raise ValueError("Not SNAP")

    data = SnapPacket()
    data.dsap = header[0]
    data.ssap = header[1]
    data.control = header[2]
    data.oui = header[3]
    data.protocol_id = header[4]
    data.parent = parent

    if data.oui == b'\x00\x00\x0C' and data.protocol_id == 0x2000:
        # Cisco Discovery Protocol
        return decode_cdp(raw[8:], data)
    return data


def decode_packet(raw):
    ethernet_hdr = struct.unpack_from('!6B 6B H', raw, 0)
    ethertype = ethernet_hdr[12]

    data = EthernetFrame()
    data.source_mac = ethernet_hdr[0:6]
    data.destination_mac = ethernet_hdr[6:12]
    data.ethertype = ethertype

    if ethertype < 1536:
        payload_start = raw[14:16]
        if payload_start == b'\xAA\xAA':
            # 802.2 SNAP
            return decode_snap(raw[14:], data)
        elif payload_start == b'\xFF\xFF':
            # Novell RAW 802.3
            pass
        else:
            # 802.2 LLC
            pass
    elif ethertype == 0x8100:
        # Tagged 802.1Q
        pass
    elif ethertype == 0x0806:
        # ARP
        pass
    elif ethertype == 0x0800:
        # IPv4
        return decode_ipv4(raw[14:], data)
    elif ethertype == 0x86DD:
        # IPv6
        pass

    return data


if __name__ == '__main__':
    with open('../dumps/lldp.bin', 'rb') as handle:
        raw = handle.read()

    packet = decode_packet(raw)
    print(packet.describe_data())
    # for opt in packet.describe_options():
    #    print(opt)

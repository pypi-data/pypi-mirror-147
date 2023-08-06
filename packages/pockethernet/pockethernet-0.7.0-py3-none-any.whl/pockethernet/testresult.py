import struct
from pockethernet.ethernet import DhcpPacket, CdpPacket


class WiremapResult:
    def __init__(self, result):
        self.connections = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.shorts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 4):
            a = (i * 2) + 1
            self.connections[a] = result[i] & 15
            self.shorts[a] = result[i + 4] & 15
            b = (i * 2) + 2
            self.connections[b] = (result[i] & 240) >> 4
            self.shorts[b] = (result[i + 4] & 240) >> 4

        self.connections[0] = result[8] & 15
        self.shorts[0] = (result[8] & 240) >> 4

        # Connections to 0 are disconnected at this point in the code, transform to None instead
        # and rewrite connections to 9 (shield) to 0 (shield in output)
        for i in range(0, len(self.connections)):
            if self.connections[i] == 0:
                self.connections[i] = None
            if self.connections[i] == 9:
                self.connections[i] = 0
            if self.shorts[i] == 0:
                self.shorts[i] = None
            if self.shorts[i] == 9:
                self.shorts[i] = 0

        if self.connections[0] == 9:
            self.connections[0] = 0

        self.wiremap_id = result[9]


class PoEResult:
    def __init__(self, result):
        self.pair_volts = result[0:4]
        self.poe_a_volt = result[4]
        self.poe_b_volt = result[5]


class LinkResult:
    def __init__(self, result):
        status, lpab, gbstatus, cssr1, gbskew, gbswap = struct.unpack('<HHHHHH', result)

        self.up = (cssr1 & 8) != 0
        self.mdix = (cssr1 & 64) != 0

        speed = (cssr1 & (16384 + 32768)) >> 14
        speeds = {
            0: "10BASE-T",
            1: "100BASE-T",
            2: "1000BASE-T"
        }
        self.speed = speeds[speed]
        self.duplex = (cssr1 & 8192) != 0

        self.link_partner_10HD = (lpab & 32) != 0
        self.link_partner_10FD = (lpab & 64) != 0
        self.link_partner_100HD = (lpab & 128) != 0
        self.link_partner_100FD = (lpab & 256) != 0
        self.link_partner_1000HD = (gbstatus & 1024) != 0
        self.link_partner_1000FD = (gbstatus & 2048) != 0

        self.skew_pair1 = (gbskew & 0xf) * 8
        self.skew_pair2 = ((gbskew & 0xff) >> 4) * 8
        self.skew_pair3 = ((gbskew & 0xfff) >> 8) * 8
        self.skew_pair4 = ((gbskew & 0xffff) >> 12) * 8


class TdrResult:
    def __init__(self, result, long_distance=False):
        self.long_distance = long_distance
        result = struct.unpack('<32H', result)

        distance = result[0:16]
        termination = result[16:]

        self.split = [False, False, False, False]
        self.split[0] = sum(distance[1:4]) > 0
        self.split[1] = distance[4] + distance[6] + distance[7] > 0
        self.split[2] = distance[8] + distance[9] + distance[11] > 0
        self.split[3] = sum(distance[12:15]) > 0

        self.distance = [0, 0, 0, 0]
        self.distance[0] = self.raw_to_dist(distance[0:4][0])
        self.distance[1] = self.raw_to_dist(distance[4:8][1])
        self.distance[2] = self.raw_to_dist(distance[8:12][2])
        self.distance[3] = self.raw_to_dist(distance[12:][3])

        if sum(self.distance) / 4 > 30.0:
            self.valid = long_distance
        else:
            self.valid = not long_distance

    def raw_to_dist(self, raw):
        if not self.long_distance:
            return (raw / 10.0 * 0.80585) - 17.335

        if raw < 105:
            return 1.0

        if raw < 120:
            return 2.0

        return raw / 10.0 * 0.7596065 - 6.180942

    def __repr__(self):
        pulse = 'long'
        if self.long_distance:
            pulse = 'short'

        avg = round(sum(self.distance) / 4)
        invalid = ''
        if not self.valid:
            invalid = ' invalid'
        return '<TDR {}: {} {} {} {}, avg: {}{}>'.format(pulse, self.distance[0], self.distance[1], self.distance[2],
                                                         self.distance[3], avg, invalid)


class TdrPlotResult(TdrResult):
    def __init__(self, result, end_distance, end_distance_meter, magic):
        self.end_distance_meter = end_distance_meter
        if end_distance > 30:
            self.short_pulse = False
        else:
            self.short_pulse = True

        point_count = int(end_distance - magic + 1)
        self.pairs = []
        for pair in range(0, 4):
            self.pairs.append([])
            for point, offset in enumerate(range(pair * point_count, (pair + 1) * point_count - 1)):
                x = self.raw_to_dist((magic + point) * 10)
                y = struct.unpack_from('<b', result, offset)[0]
                self.pairs[pair].append((x, y))

    def __repr__(self):
        return '<TDRPlot {} meter>'.format(self.end_distance_meter)


class DhcpResult:
    def __init__(self, packet):
        if not isinstance(packet, DhcpPacket):
            raise ValueError("Unexpected packet")
        self.client_ip = packet.ciaddr
        self.your_ip = packet.yiaddr
        self.next_server = packet.siaddr
        self.gateway = packet.giaddr
        self.filename = packet.file
        self.lease_time = None
        self.subnet_mask = None
        self.nameservers = None
        decoded = packet.describe_options()
        self.options_list = decoded
        self.options = {}
        for tag, name, value in decoded:
            self.options[tag] = value
            if tag == 1:
                self.subnet_mask = value
            elif tag == 3:
                self.gateway = value
            elif tag == 51:
                self.lease_time = value
            elif tag == 6:
                self.nameservers = value


class CdpResult:
    def __init__(self, packet):
        if not isinstance(packet, CdpPacket):
            raise ValueError("Unexpected packet")

        self.fields = {}
        self.field_list = packet.describe_data()
        for type, name, data in self.field_list:
            self.fields[name] = data
        self.ttl = packet.ttl


class BerResult:
    def __init__(self, result):
        self.sent, self.received, self.errors, status = struct.unpack('<3HB', result)
        self.status = status == 4

import argparse
import logging
from pockethernet import Pockethernet, WiremapResult, PoEResult, LinkResult, PHY_ADVERTIZE_100BASET, TdrResult, \
    DhcpResult, CdpResult


def print_wiremap(wiremap):
    if not isinstance(wiremap, WiremapResult):
        return

    for i in range(0, len(wiremap.connections)):
        if wiremap.connections[i] is None:
            wiremap.connections[i] = 0
        if wiremap.shorts[i] is None:
            wiremap.shorts[i] = 0

    if sum(wiremap.connections) == 0 and sum(wiremap.shorts) == 0:
        print("All connections open (no cable inserted, no wiremap adapter connected or full break)")
        return

    if sum(wiremap.connections) == 0 and wiremap.shorts == [0, 3, 6, 0, 7, 8, 0, 0, 0]:
        print("Wiremap adapter inserted wrong way around")
        return

    if sum(wiremap.connections) == 0 and wiremap.shorts == [0, 2, 0, 1, 1, 1, 1, 1, 1]:
        print("Cable inserted into ethernet port")
        return

    if sum(wiremap.shorts) > 0:
        print("Cable shorted")
        return

    if wiremap.connections == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        print("Straight cable")
        return

    if wiremap.connections == [0, 8, 7, 6, 5, 4, 3, 2, 1]:
        print("Rollover cable (for serial console")
        return

    print("Unknown or wrong cable")


def print_poe(poe):
    if not isinstance(poe, PoEResult):
        return

    print("Pair voltages:")
    for v in poe.pair_volts:
        print("- {}V".format(v))
    print("PoE A: {}V".format(poe.poe_a_volt))
    print("PoE B: {}V".format(poe.poe_b_volt))


def print_link(link):
    if not isinstance(link, LinkResult):
        return

    if not link.up:
        print("No link established")
        return

    duplexity = "half duplex"
    if link.duplex:
        duplexity = "full duplex"
    print("Got {} {} link".format(link.speed, duplexity))

    print("Link partner advertises:")
    print("            HD  FD")
    print("  10 MBIT   {:d}   {:d}".format(link.link_partner_10HD, link.link_partner_10FD))
    print(" 100 MBIT   {:d}   {:d}".format(link.link_partner_100HD, link.link_partner_100FD))
    print("1000 MBIT   {:d}   {:d}".format(link.link_partner_1000HD, link.link_partner_1000FD))


def print_tdr(tdr):
    if not isinstance(tdr, TdrResult):
        return

    if not tdr.valid:
        print("TDR result is inconclusive")

    print("Cable length: {}m".format(round(sum(tdr.distance) * 10 / 4) / 10))
    for i, d in enumerate(tdr.distance):
        print("  Pair {}: {}m".format(i + 1, round(d * 100) / 100))


def print_dhcp(packet):
    if not isinstance(packet, DhcpResult):
        return

    print(f"DHCP {packet.options[53]}")
    print(f"  DHCP Server: {packet.options[54]}")
    print(f"  Address: {packet.your_ip}")
    if 1 in packet.options:
        print(f"  Subnet Mask: {packet.options[1]}")
    if 3 in packet.options:
        line = []
        for addr in packet.options[3]:
            line.append(str(addr))
        print(f"  Gateway: {', '.join(line)}")
    else:
        print("  Gateway: not set")
    if 6 in packet.options:
        line = []
        for addr in packet.options[6]:
            line.append(str(addr))
        print(f"  DNS: {', '.join(line)}")
    else:
        print("  DNS: not set")
    print("")
    print("  All options:")
    for tag, name, value in packet.options_list:
        print(f"    {str(tag).ljust(3)} {name} = {value}")


def print_cdp(packet):
    if not isinstance(packet, CdpResult):
        return

    print("CDP packet")
    if packet.ttl is not None:
        print(f"  ttl = {packet.ttl}")
    for type, name, data in packet.field_list:
        print(f"  {name} = {data}")


def main():
    parser = argparse.ArgumentParser(description='Pockethernet shell client')
    parser.add_argument('mac', help='Bluetooth MAC of the Pockethernet')
    parser.add_argument('--debug', help='Enable debug output', action='store_true')
    parser.add_argument('tests', metavar='test', nargs='*', default=['wiremap', 'poe', 'link'])
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    client = Pockethernet()
    client.connect(args.mac)
    client.link_reset()

    logging.debug('Test queue: ' + ', '.join(args.tests))

    for test in args.tests:
        if test == 'wiremap':
            wiremap = client.get_wiremap()
            print_wiremap(wiremap)
        elif test == 'poe':
            print_poe(client.get_poe())
        elif test == 'link':
            print_link(client.get_link())
        elif test == 'tdr':
            tdr = client.get_tdr(False)
            if not tdr.valid:
                tdr = client.get_tdr(True)
            print_tdr(tdr)
        elif test == 'layer3':
            client.set_vlan(-1)
            client.set_capture_mode(dhcp=True, lldp=True)
            client.enable_dhcp()
            client.get_link(speed=PHY_ADVERTIZE_100BASET)
            while True:
                packet = client.wait_for_capture_results()
                if isinstance(packet, DhcpResult):
                    print_dhcp(packet)
                elif isinstance(packet, CdpResult):
                    print_cdp(packet)
                else:
                    print(packet)


if __name__ == '__main__':
    main()

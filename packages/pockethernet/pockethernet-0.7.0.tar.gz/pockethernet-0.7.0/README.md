# Pockethernet Protocol reverse-engineering

Because I want a desktop app

## Contents

* Panasonic PAN1026 Bluetooth 4.0/BLE module
* 3.3V <-> 5V UART level shifter
* STM32F207 main MCU
* TI TLC59116 i2c controlled led driver
* Marvell 88E1111 Gigabit ethernet transceiver
* TPS65217x PMIC/Battery controller

## Protocol

You need the latest firmware (I'm using v29) so the device uses BLE GATT instead of BT4 RFCOMM. 

It provides the Generic Access service (0x1800) and a vendor specific service 59710d3d-d96a-4666-ac17-e7f61ba52480 and
the characteristic 6c741b59-f88f-4a3f-a5c4-2223d2958378

| name | command | response type | details |
| --- | --- | --- | --- |
| device info | 1 | 4097 | device info |
| ?        | 2 | 4098 | 24 bytes b'\x00\x00\x00\x00\x02\x11\x11\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x0c\x00\x0c\x00\x0c' and relais clicks a few times |
| get link | 3 | 4099 |link data |
| ?        | 4 | 4100 | 20 bytes |
| get wiremap | 48 | 4144 | 10 bytes wiremap data |
| get poe | 49 | 4145 | 6 bytes poe data |
| connect | 52 | 4097 |same link data |
| 

## Command 1: get device info

Command 1 takes no parameters and returns the hardware revision, firmware version and mac address.

| offset | example | description |
| --- | --- | --- |
| 0 | 58 | 6th byte of the MAC address |
| 1 | 3 | 5th byte of the MAC address |
| 2 | 9 | 4th byte of the MAC address |
| 3 | 0 | ? |
| 4 | 4 | Hardware revision number |
| 5 | 29 | Firmware revision number |

The first 3 bytes of the MAC address is always 28:FD:80

## Command 48: get wiremap

The main function of the tester, returns the wire map measurement result from a test with a wiremap adapter.

| offset | example | description |
| --- | --- | --- |
| 0 | 33 | connections wire 1 and 2 |
| 1 | 67 | connections wire 3 and 4 |
| 2 | 101 | connections wire 5 and 6 | 
| 3 | 135 | connections wire 7 and 8 |
| 4 | 0 | shorts wire 1 and 2 |
| 5 | 0 | shorts wire 3 and 4 |
| 6 | 0 | shorts wire 5 and 6 |
| 7 | 0 | shorts wire 7 and 8 |
| 8 | 0 | shield connections and shorts |
| 9 | 0 | wiremap ID |

Each byte except the last is used as two groups of four bits. Every 4 bit number is a reference to which wire number
the current wire is connected on the wiremap adapter side or the number it is shorted to on the pockethernet side. 

The first byte for example is 33, or 0x21 in hex, if split into two 4-bit numbers then those are `1` and `2`. This means
that the first wire on the pockethernet side is wired to the first wire on the wiremap adapter side. If the first 4 bytes
end up as 1, 2, 3, 4, 5, 6, 7, 8 then that means that it's a straight cable. In cases where the ethernet cable has
shielding connected then the shield is counted as the 9th wire. 

The 4th byte is the shorts for the first two wires. Since it's 0 for both nibbles it means that it's not shorted at all. 

The 8th byte is the 4-bit connection number and 4-bit short number for the shield wire packed into a single byte.

The 9th byte is the wiremap ID, this should be 1 for the supplied wiremap adapter but so far this hasn't been observed
above zero.

## Command 49: get PoE data

The pockethernet can measure passive power supplied on all pairs or 802.3af power.

| offset | example | description |
| --- | --- | --- |
| 0 | 0 | Voltage on pair 1 |
| 1 | 0 | Voltage on pair 2 |
| 2 | 13 | Voltage on pair 3 | 
| 3 | 0 | Voltage on pair 4 |
| 4 | 0 | Voltage between pair 1-2 and pair 3-6 (802.3af mode a) |
| 4 | 23 | Voltage between pair 4-5 and pair 7-8 (802.3af mode a) |

The values of the bytes are whole volts as decimal
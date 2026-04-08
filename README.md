# Kernelcon 26: All Keys Lost: A Car Hacking Adventure
## msd80-isn-sniffer
 
CAN bus sniffer and capture logs from the "All Keys Lost: A Car Hacking Journey" talk at KernelCon 2026.
 
This repo contains the Python sniffer used to capture UDS diagnostic traffic between an Autel IM508S and a bench-mounted BMW MSD80 DME, along with the raw capture logs and analysis notes from the session.
 
---
 
## What This Is
 
The MSD80 is a Siemens/Continental DME used in the BMW N54 engine (E90/E92 335i, E60 535i, E71 X6 35i and others). It communicates over PT-CAN at 500kbps and uses UDS (ISO 14229) over ISO-TP for diagnostic and programming functions including ISN read and security access.
 
This tool passively sniffs the CAN bus while a diagnostic tool performs an ISN read, capturing the full transaction so you can see exactly what is happening under the hood of a commercial key programming tool.
 
---
 
## Hardware Requirements
 
- **CANable 2.0** or compatible gs_usb device (tested with DSD TECH SH-C31G isolated variant)
- Bench harness for the MSD80 with 12V supply on connector A pins 1 and 46, ground on connector A pin 6
- CAN-H and CAN-L tapped from connector B pins 27 and 48 respectively
- Termination resistors: 120 ohm across CAN-H and CAN-L at each end of the bus. Do NOT enable the onboard termination resistor on the CANable when sniffing inline, you will have three terminators on the bus and it will cause communication errors
 
---
 
## Software Requirements
 
### Linux / WSL2
 
```bash
pip install python-can
sudo modprobe can
sudo modprobe can_raw
sudo modprobe gs_usb
sudo ip link set can0 up type can bitrate 500000
```
 
### WSL2 Note
 
The Microsoft standard WSL2 kernel does not ship with gs_usb support. You will need to compile a custom kernel with the following options enabled:
 
```
CONFIG_CAN=m
CONFIG_CAN_RAW=m
CONFIG_CAN_DEV=m
CONFIG_CAN_GS_USB=m
```
 
Clone the WSL2 kernel source, copy `Microsoft/config-wsl` to `.config`, append those four lines, run `make olddefconfig` then `make -j$(nproc)`. After `sudo make modules_install`, point WSL at the new kernel via `.wslconfig` in your Windows home directory.
 
## Usage
 
```bash
python3 sniffer.py [output_file]
```
 
If no output file is specified it defaults to `msd80_capture.log`. Run the sniffer first, then trigger the ISN read on your diagnostic tool. Hit Ctrl+C when the read completes.
 
```bash
# Default output file
python3 sniffer.py
 
# Named output file
python3 sniffer.py my_capture.log
```
 
---
 
## Capture Log Format
 
Each line is a single CAN frame:
 
```
<timestamp> <arbitration_id> <data_hex>
1775600027.439832 0x7e0 0154fd776c48d990
1775600027.533078 0x7e8 1089a00000000100
```
 
### CAN IDs You Will See
 
| ID | Direction | Protocol |
|----|-----------|----------|
| `0x6f1` | Tester to DME | BMW KWP2000 physical addressing |
| `0x612` | DME to Tester | BMW KWP2000 response |
| `0x7e0` | Tester to DME | UDS diagnostic (ISO 14229) |
| `0x7e8` | DME to Tester | UDS response |
| `0x140` | Tester keepalive | GoBox3 heartbeat |
 
---
 
## What the Captures Show
 
The ISN read transaction follows this sequence every time:
 
1. KWP session establishment on `0x6f1/0x612`
2. UDS extended diagnostic session request on `0x7e0`
3. Security access key exchange, tester sends a static 8 byte key
4. DME responds with a 137 byte encrypted payload via ISO-TP multi-frame transfer
5. On successful reads the Autel decrypts the payload and returns the ISN and chip password
 
The 137 byte response changes on every attempt due to session-based encryption even though the key sent by the tester is static. This is documented in the capture logs.
 
---
 
## Repo Contents
 
```
sniffer.py          CAN sniffer script
captures/           Raw capture logs from bench sessions
  msd80_*.log       Individual capture sessions
README.md           This file
```
 
---
 
## Talk
 
This tool was built as part of the "All Keys Lost: A Car Hacking Journey" talk presented at KernelCon 2026 in Omaha, NE.
 
**@f8al / @SecurityShrimp**
https://linktr.ee/f8al
 
---
 
## Disclaimer
 
This tool is for educational and research purposes. All testing was performed on hardware owned by the researcher. Do not use this on vehicles you do not own.

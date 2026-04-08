#!/bin/env python3
import can
import signal
import sys

bus = can.interface.Bus(interface='socketcan', channel='can0', bitrate=500000)

print("Sniffing on can0 at 500kbps, run your Autel ISN read now...")
print("Ctrl+C to stop capture\n")

def shutdown(sig, frame):
    print("\nCapture stopped")
    bus.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

capfile = sys.argv[1] if len(sys.argv) > 1 else 'dme_can_capture.cap'

with open(capfile, 'w') as f:
    for msg in bus:
        line = f"{msg.timestamp:.6f} {hex(msg.arbitration_id)} {msg.data.hex()}"
        print(line)
        f.write(line + '\n')import can
import signal
import sys

bus = can.interface.Bus(interface='socketcan', channel='can0', bitrate=500000)

print("Sniffing on can0 at 500kbps, run your Autel ISN read now...")
print("Ctrl+C to stop capture\n")

def shutdown(sig, frame):
    print("\nCapture stopped")
    bus.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

with open('msd80_capture.log', 'w') as f:
    for msg in bus:
        line = f"{msg.timestamp:.6f} {hex(msg.arbitration_id)} {msg.data.hex()}"
        print(line)
        f.write(line + '\n')

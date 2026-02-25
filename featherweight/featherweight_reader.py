# This script reads feather weight GPS data from a serial port, filters for lines matching 
# the specific pattern of featherweight data, and writes the filtered data to a log file. It also prints 
# the matched lines to the console. The script handles serial port exceptions 
# and allows for graceful termination with a keyboard interrupt.

import serial
import re
import sys

PORT_NAME = 'COM4'
ser = None
file = "raw_gps_data.log"

try:
    ser = serial.Serial(PORT_NAME, 115200, timeout=1)
    print(f"Successfully opened port: {ser.port}", file=sys.stderr)

except serial.SerialException as e:
    print(f"Error opening port {PORT_NAME}: {e}", file=sys.stderr)
    exit()

try:
    regex = re.compile(r"@ GPS_STAT.*CRC: [0-9A-F]{4}")
    output = open(file, "w", encoding='utf-8')
    while True:
        if ser.in_waiting > 0:
            line = ser.read(ser.in_waiting)
            line_str = line.decode('ascii', errors='replace').strip()
            match = regex.search(line_str)
            if match:
                print(match.group(0), flush=True)
                output.write(match.group(0) + '\n')
                output.flush()
            # print(line_str)
            # output.write(line_str)
                
except KeyboardInterrupt:
    print("\nStopping data read", file=sys.stderr)

finally: 
    if ser.is_open:
        ser.close()
    if output:
        output.close()
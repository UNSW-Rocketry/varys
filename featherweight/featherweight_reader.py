import serial
import re

PORT_NAME = 'COM3'
ser = None

try:
    ser = serial.Serial(PORT_NAME, 115200, timeout=1)
    print(f"Successfully opened port: {ser.port}")

except serial.SerialException as e:
    print(f"Error opening port {PORT_NAME}: {e}")
    exit()

try:
    regex = re.compile(r"@ GPS_STAT.*CRC: [0-9A-F]{4}")
    output = open("log_eveg.txt", "w", encoding='utf-8')
    while True:
        if ser.in_waiting > 0:
            line = ser.read(ser.in_waiting)
            line_str = line.decode('ascii', errors='replace').strip()
            match = regex.search(line_str)
            if match:
                print(match.group(0))
                output.write(match.group(0))
            # print(line_str)
            # output.write(line_str)
                
except KeyboardInterrupt:
    print("\nStopping data read")

finally: 
    if ser.is_open:
        ser.close()
    if output:
        output.close()
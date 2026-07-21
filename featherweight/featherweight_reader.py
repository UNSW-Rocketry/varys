# This script reads feather weight GPS data from a serial port, filters for lines matching 
# the specific pattern of featherweight data, and writes the filtered data to a log file. It also prints 
# the matched lines to the console. The script handles serial port exceptions 
# and allows for graceful termination with a keyboard interrupt.

#import serial
import re
import sys

PORT_NAME = 'COM4'
ser = None
#file = "raw_gps_data.log"
file = "gps_output.log"

class StdinSerial:
    """Mimics the bits of serial.Serial that the reader uses, backed by stdin."""
    port = "<stdin>"
    is_open = True

    @property
    def in_waiting(self):
        return 1  # pretend there's always data; read() will block until there is

    def read(self, size=1):
        return sys.stdin.buffer.read(size)

    def readline(self):
        return sys.stdin.buffer.readline()

    def close(self):
        self.is_open = False

if '--stdin' in sys.argv:
    ser = StdinSerial()
    print("Reading from stdin", file=sys.stderr)
else:
    try:
        ser = serial.Serial(PORT_NAME, 115200, timeout=1)
        print(f"Successfully opened port: {ser.port}", file=sys.stderr)

    except serial.SerialException as e:
        print(f"Error opening port {PORT_NAME}: {e}", file=sys.stderr)
        exit()

output = None


class Regexish:

    def compile_rule(self, pattern):
        """Compile a regex pattern for matching featherweight GPS data lines."""

        self.pattern = ["".join(entry.split()) if isinstance(entry, str) else entry for entry in pattern]
        print(self.pattern)
        self.data_stream = []
        self.start_str = ""
        self.end_str = ""
        self.logging = False

        return None

    def match_line(self, line):
        """Check if a line matches the compiled regex pattern."""
        
        if self.pattern[2]:
            parity_bytes = self.pattern[3]
        else:
            parity_bytes = -len(self.end_str)

        if self.logging:
            self.end_str += line
            #print(self.end_str + " ===> " + self.pattern[1])
        else:
            self.start_str += line

        if self.logging == True:
            self.data_stream += line

        """------------------------LOGIC FOR FIND THE START------------------------"""
        if len(self.start_str) >= len(self.pattern[0]) and self.start_str[-len(self.pattern[0]):] == self.pattern[0]:
            self.logging = True
            #print("FOUND GPS STAT")
            self.data_stream += self.start_str[-len(self.pattern[0]):]
            self.start_str = ""

        """------------------------LOGIC FOR FIND THE END------------------------"""
        if len(self.end_str) >= len(self.pattern[1])+parity_bytes and self.end_str[-(len(self.pattern[1]) + parity_bytes):-parity_bytes] == self.pattern[1]:
            self.logging = False
            #print("FOUND CRC END")
            #print(self.data_stream)
            result = "".join(self.data_stream)   # list of chars -> string
            self.data_stream = []                # reset to empty list
            self.start_str = ""
            self.end_str = ""
            return result

        return None



try:
    #regex = re.compile(r"@ GPS_STAT.*CRC: [0-9A-F]{4}")
    regex = Regexish()
    regex.compile_rule(["@ GPS_STAT", "CRC:", 1, 4])
    output = open(file, "w", encoding='utf-8')
    while True:
        if ser.in_waiting > 0:
            line = ser.read(ser.in_waiting)
            line_str = line.decode('ascii', errors='replace').strip()
            #print(line_str)
            match = regex.match_line(line_str)
            if match:
                print(match)
                #print(match.group(0), flush=True)
                output.write(match + '\n')
                output.flush()
            # print(line_str)
            # output.write(line_str)
            # Change to read character by character
            

except KeyboardInterrupt:
    print("\nStopping data read", file=sys.stderr)

finally:
    if ser and ser.is_open:
        ser.close()
    if output:
        output.close()
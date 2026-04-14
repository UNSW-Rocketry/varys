# This file will contain two key functions that will allow us to
# parse data from our Featherweight GPS Tracker.

import json
import logging
import sys
from datetime import date
import time

logging.basicConfig(level=logging.WARNING)

print("Parser running", file=sys.stderr)

file_path = "packets.csv"





def parse_data_line_to_dict(line: str, tracker_id: int):
    """
    This function serves the primary purpose of converting data from the Featherweight
    GPS Tracker into a human-readable format. Please note it only converts one
    row entry at a time into a valid dictionary.
    This does need to be updated to be more robust. Function does incorporate the use
    of "N" offsets. We must cater for when additional flags and bits are added.
    Input: The line read in from the file which marks one entry from the GPS tracker.
    Output: Returns either a valid python dictionary or None.
    """
    tokens = line.strip().split(",")

    #print(tokens)
    #print("Tokens length: ", len(tokens))

    #if "!" not in tokens or "/A=" not in tokens:
        #uncomment later
        #logging.warning("Dropped line: missing GPS_STAT or CRC_OK: %r", line)
        #return None
    
    fields = {
        "timestamp": None,
        "packet_id": None,
        "altitude": None,
        "latitude": None,
        "longitude": None,
    }

    if len(tokens) == 2:
            fields["timestamp"] = tokens[0]
            fields["packet_id"] = f"{unique_packet_id}"
    else:
        logging.warning("Dropped line: missing GPS_STAT or CRC_OK: %r", line)
        return None


    for i, char in enumerate(tokens[1]):
        if char == "!":
            lat = ""
            i += 1
            while i < len(tokens[1]) and tokens[1][i] != "/":
                    lat += tokens[1][i]
                    if tokens[1][i] == "\ufffd":
                        lat = None
                        break
                    i += 1
                    

            fields["latitude"] = lat
            print("Latitude: ", lat)

        elif char == "/" and tokens[1][i - 1] != "-":
            long = ""
            i += 1
            while i < len(tokens[1]) and tokens[1][i] != "-":
                long += tokens[1][i]
                if tokens[1][i] == "\ufffd":
                    long = None
                    break
                i += 1

            fields["longitude"] = long
            print("Longitude: ", long)


        elif char == "=" and len(tokens[1]) > i + 1:
            alt = ""
            i += 1
            while i < len(tokens[1]) and tokens[1][i] != "*":
                alt += tokens[1][i]
                if tokens[1][i] == "\ufffd":
                    alt = None
                    break
                i += 1

            fields["altitude"] = alt
            print("Altitude: ", alt)

    missing = [key for key, value in fields.items() if value is None]

    if missing:
        logging.warning(
            "Dropped line: missing fields %s in packet: %r", 
            missing, line
        )
        return None

    return fields


def tail_file(file_path):
    with open(file_path, 'r') as file:
        file.seek(0, 2) # Go to the end of the file
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1) # Wait for more data
                continue
            yield line.strip()
            


unique_packet_id = 0
tail_file_gen = tail_file(file_path)
for line in tail_file_gen:
    parsed_packet = parse_data_line_to_dict(line, unique_packet_id)
    unique_packet_id += 1
    
    if parsed_packet:
        # We can now print to a file instead of stdout
        with open('parsed_packet_data.jsonl', 'a') as f:
            f.write(json.dumps(parsed_packet, separators=(',', ':')) + '\n')
            f.flush()


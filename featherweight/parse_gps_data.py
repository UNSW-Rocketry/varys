# This file will contain two key functions that will allow us to
# parse data from our Featherweight GPS Tracker.

import json
import logging

logging.basicConfig(level=logging.WARNING)

def parse_data_line_to_dict(line: str) -> dict[str, any] | None:
    """
    This function serves the primary purpose of converting data from the Featherweight
    GPS Tracker into a human-readable format. Please note it only converts one
    row entry at a time into a valid dictionary.

    This does need to be updated to be more robust. Function does incorporate the use
    of "N" offsets. We must cater for when additional flags and bits are added.

    Input: The line read in from the file which marks one entry from the GPS tracker.
    Output: Returns either a valid python dictionary or None.
    """
    tokens = line.strip().split()

    if "GPS_STAT" not in tokens or "CRC_OK" not in tokens:
        logging.warning("Dropped line: missing GPS_STAT or CRC_OK: %r", line)
        return None

    fields = {
        "timestamp":          None,
        "tracker_id":         None,
        "altitude":           None,
        "latitude":           None,
        "longitude":          None,
        "vel_horizontal_fps": None,
        "vel_vertical_fps":   None,
        "heading_deg":        None,
        "fix":                None,
        "sats_total":         None,
        "sats_ge24_dbhz":     None,
        "sats_ge32_dbhz":     None,
        "sats_ge40_dbhz":     None,
    }

    for i, token in enumerate(tokens):
        if token == "GPS_STAT" and len(tokens) > i + 5:
            fields["timestamp"] = f"{tokens[i + 2]}-{tokens[i + 3]}-{tokens[i + 4]}T{tokens[i + 5]}Z"

        elif token == "TRK" and len(tokens) > i + 2:
            fields["tracker_id"] = f"{tokens[i + 1]}-{tokens[i + 2]}"

        elif token == "Alt" and len(tokens) > i + 1:
            fields["altitude"] = float(tokens[i + 1])

        elif token == "lt" and len(tokens) > i + 1:
            fields["latitude"] = float(tokens[i + 1])

        elif token == "ln" and len(tokens) > i + 1:
            fields["longitude"] = float(tokens[i + 1])
            
        elif token == "Vel" and len(tokens) > i + 3:
            fields["vel_horizontal_fps"] = float(tokens[i + 1])
            fields["heading_deg"] = float(tokens[i + 2])
            fields["vel_vertical_fps"] = float(tokens[i + 3])

        elif token == "Fix" and len(tokens) > i + 6:
            fields["fix"] = int(tokens[i + 1])
            fields["sats_total"] = int(tokens[i + 3])
            fields["sats_ge24_dbhz"] = int(tokens[i + 4])
            fields["sats_ge32_dbhz"] = int(tokens[i + 5])
            fields["sats_ge40_dbhz"] = int(tokens[i + 6])

    missing = [key for key, value in fields.items() if value is None]
    
    if missing:
        logging.warning(
            "Dropped line: missing fields %s in packet: %r", 
            missing, line
        )
        return None
        
    return fields
        
with open("gps_output.jsonl", "w") as outfile:
    for line in open("log_gps.txt"):
        rec = parse_data_line_to_dict(line)
        if rec:
            json.dump(rec, outfile)
            outfile.write("\n")
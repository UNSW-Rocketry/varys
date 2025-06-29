# This file will contain two key functions that will allow us to
# parse data from our Featherweight GPS Tracker.

import json

YEAR_OFFSET = 2
MONTH_OFFSET = 3
DAY_OFFSET = 4
TIME_OFFSET = 5
ALT_OFFSET = 1
LATITUDE_OFFSET = 1
LONGITUDE_OFFSET = 1
HORIZONTAL_VELOCITY_OFFSET = 1
HORIZONTAL_HEADING_OFFSET = 2
UPWARD_VELOCITY_OFFSET = 3
SATELLITE_FIX_OFFSET = 3
SATELLITES_GREATER_THAN_24_DB = 4
SATELLITES_GREATER_THAN_32_DB = 5
SATELLITES_GREATER_THAN_40_DB = 6



def parse_data_line_to_json(line: str) -> dict[str, any] | None:
    tokens = line.strip().split()
    json_dict = {}

    for i, token in enumerate(tokens):
        if token == "GPS_STAT" and len(tokens) > i + TIME_OFFSET:
            timestamp = f"{tokens[i + YEAR_OFFSET]}-{tokens[i + MONTH_OFFSET]}-{tokens[i + DAY_OFFSET]}T{tokens[i + TIME_OFFSET]}Z"
            json_dict["timestamp"] = timestamp
            
        elif token == "Alt" and len(tokens) > i + ALT_OFFSET:
            altitude = float(tokens[i + ALT_OFFSET])
            json_dict["altitude"] = altitude # Note this is in feet as per the manual.

        elif token == "lt" and len(tokens) > i + LATITUDE_OFFSET:
            latitude = float(tokens[i + LATITUDE_OFFSET])
            json_dict["latitude"] = latitude

        elif token == "ln" and len(tokens) > i + LONGITUDE_OFFSET:
            longitude = float(tokens[i + LONGITUDE_OFFSET])
            json_dict["longitude"] = longitude

        elif token == "Vel" and len(tokens) > i + UPWARD_VELOCITY_OFFSET:
            horizontal_velocity = float(tokens[i + HORIZONTAL_VELOCITY_OFFSET])
            horizontal_heading = float(tokens[i + HORIZONTAL_HEADING_OFFSET])
            upward_velocity = float(tokens[i + UPWARD_VELOCITY_OFFSET])
            
            json_dict["horizontal_velocity"] = horizontal_velocity
            json_dict["horizontal_heading"] = horizontal_heading
            json_dict["upward_velocity"] = upward_velocity

        elif token == "Fix" and len(tokens) > i + SATELLITE_FIX_OFFSET:
            total_satellites = int(tokens[i + SATELLITE_FIX_OFFSET])
            num_sats_24_db = int(tokens[i + SATELLITES_GREATER_THAN_24_DB])
            num_sats_32_db = int(tokens[i + SATELLITES_GREATER_THAN_32_DB])
            num_sats_40_db = int(tokens[i + SATELLITES_GREATER_THAN_40_DB])

            
            json_dict["total_satellites"] = total_satellites
            json_dict["sats_ge24_dbhz"] = num_sats_24_db
            json_dict["sats_ge32_dbhz"] = num_sats_32_db
            json_dict["sats_ge40_dbhz"] = num_sats_40_db

        

        
    print(json.dumps(json_dict, indent=4))
    #print(newLine)
    return None

with open("log_gps.txt", "r") as file:
    for line in file:
        #print(line, end="")
        parse_data_line_to_json(line)
        break
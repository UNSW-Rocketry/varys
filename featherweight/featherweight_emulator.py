# nb this will append stuff to raw_gps_data.log

from datetime import datetime
import time
import random

file = "raw_gps_data.log"

lat = -33.4294884592
lon = 150.96568
alt = 120

for _ in range(1000):

    # simulate rocket movement
    alt += random.uniform(0.5, 2)
    lat += random.uniform(-0.000005, 0.000005)
    lon += random.uniform(-0.000005, 0.000005)

    vel_h = random.randint(0, 30)
    heading = random.randint(0, 360)
    vel_v = random.randint(-5, 40)

    sats_total = random.randint(10, 14)

    now = datetime.utcnow()
    timestamp = now.strftime("%H:%M:%S.%f")[:-3]  # match featherweight format

    line = (
        f"@ GPS_STAT 208 0000 00 00 {timestamp} CRC_OK "
        f"TRK UNSWRT T2 "
        f"Alt {alt:06.0f} "
        f"lt {lat:.10f} "
        f"ln {lon:+.5f} "
        f"Vel {vel_h:+04d} {heading:+03d} {vel_v:+04d} "
        f"Fix 3 # {sats_total} 10 5 2 "
        f"000_00_00 000_00_00 000_00_00 000_00_00 000_00_00 "
        f"CRC: 3CBE"
    )

    with open(file, "a") as f:
        f.write(line + "\n")

    print(line)

    time.sleep(0.1)
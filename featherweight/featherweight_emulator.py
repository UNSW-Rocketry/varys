from datetime import datetime
import time
with open("output.txt", "w") as myFile:
    for x in range(100):
        curr_time = datetime.now()
        myFile.write('@ GPS_STAT 208 0000 00 00 ' + str(curr_time.time()) + ' CRC_OK  TRK UNSWRT T2   Alt 000121 lt -33.4294884592 ln +150.96568 Vel +0000 +113 +0000 Fix 3 # 13 10  5  2 000_00_00 000_00_00 000_00_00 000_00_00 000_00_00 CRC: 3CBE\n')
        time.sleep(0.1)

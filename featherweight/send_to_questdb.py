import json
from datetime import datetime, timezone
from questdb.ingress import Sender, Protocol, TimestampNanos
import time

HOST = "localhost"
PORT = 9009
file = "parsed_gps_data.jsonl"

def to_nanos(ts: str) -> int:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1_000_000_000)

def tail_file(file_path):
    with open(file_path, 'r') as file:
        file.seek(0, 2)  # Go to the end of the file
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)  # Wait for more data
                continue
            yield line.strip()

def main():
    with Sender(Protocol.Tcp, HOST, PORT) as sender:
        # with open("gps_output.jsonl") as fp:
            # for line in fp:
        # for line in sys.stdin:
        #     rec = json.loads(line)
        for line in tail_file(file):
            # try:
            rec = json.loads(line)
            if not rec:
                continue
            try:
                ts_nanos = to_nanos(rec.pop("timestamp"))
            except (KeyError, ValueError):
                continue
            tags = {"tracker_id": rec.pop("tracker_id", "unknown")}
            sender.row(
                "gps_data",
                symbols=tags,
                columns=rec,
                at=TimestampNanos(ts_nanos)
            )
        sender.flush()

if __name__ == "__main__":
    main()
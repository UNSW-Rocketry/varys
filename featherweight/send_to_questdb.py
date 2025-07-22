import json
from datetime import datetime, timezone
from questdb.ingress import Sender, Protocol, TimestampNanos

HOST = "localhost"
PORT = 9009

def to_nanos(ts: str) -> int:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1_000_000_000)

def main():
    with Sender(Protocol.Tcp, HOST, PORT) as sender:
        with open("gps_output.jsonl") as fp:
            for line in fp:
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
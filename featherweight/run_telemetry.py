import os
import signal
import socket
import subprocess
import sys
import time


QUESTDB_HOST = os.getenv("QUESTDB_HOST", "questdb")
QUESTDB_PORT = int(os.getenv("QUESTDB_PORT", "9009"))
TELEMETRY_SOURCE = os.getenv("TELEMETRY_SOURCE", "emulator")

processes = []
stopping = False


def stop_processes(_signal=None, _frame=None):
    global stopping
    stopping = True


def wait_for_questdb():
    print(
        f"Waiting for QuestDB at {QUESTDB_HOST}:{QUESTDB_PORT}",
        flush=True,
    )

    while not stopping:
        try:
            with socket.create_connection(
                (QUESTDB_HOST, QUESTDB_PORT),
                timeout=2,
            ):
                print("QuestDB is ready", flush=True)
                return True
        except OSError:
            time.sleep(2)

    return False


signal.signal(signal.SIGINT, stop_processes)
signal.signal(signal.SIGTERM, stop_processes)

open("raw_gps_data.log", "a", encoding="utf-8").close()
open("parsed_gps_data.jsonl", "a", encoding="utf-8").close()

if not wait_for_questdb():
    sys.exit(0)

processes.append(
    subprocess.Popen([sys.executable, "-u", "parse_gps_data.py"])
)
processes.append(
    subprocess.Popen([sys.executable, "-u", "send_to_questdb.py"])
)

time.sleep(1)

if TELEMETRY_SOURCE == "reader":
    source_script = "featherweight_reader.py"
else:
    source_script = "featherweight_emulator.py"

print(f"Starting telemetry source: {source_script}", flush=True)

processes.append(
    subprocess.Popen([sys.executable, "-u", source_script])
)

exit_code = 0

while not stopping:
    for process in processes:
        if process.poll() is not None:
            print(
                f"A telemetry process exited with code "
                f"{process.returncode}",
                file=sys.stderr,
                flush=True,
            )
            exit_code = 1
            stopping = True
            break

    time.sleep(0.5)

for process in processes:
    if process.poll() is None:
        process.terminate()

for process in processes:
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

sys.exit(exit_code)
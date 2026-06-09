import socket, csv, datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 9999))  # match the port in SDRangel

with open("packets.csv", "a", newline="") as f:
    writer = csv.writer(f)
    while True:
        data, addr = sock.recvfrom(4096)
        writer.writerow([datetime.datetime.now(), data.decode("utf-8", errors="replace")])
        f.flush()
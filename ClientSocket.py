import socket
import time

UDP_IP = "73.37.174.96"
UDP_PORT = 9652

client_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Listening...")
# TODO do this with a configurable delay period
while True:
    encode_string = ""
    data = client_conn.sendto(str.encode('ping'), (UDP_IP, UDP_PORT))

    rcv_data = client_conn.recvfrom(1024)
    send_time = int(str(rcv_data[0].decode()).split()[1])
    diff = (time.time_ns() - send_time) * 1000
    print(f"time difference from sender: {diff}ms")

    #TODO add timeout after no received messages
import socket
import time

# test variables
MESSAGE = "Hello World!"
UDP_PORT = 9652
UDP_IP = "192.168.1.124"  # use the localhost loopback for now

# establish socket object. SOCK_DGRAM indicates a UDP data frame, stored in a static context.
conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.bind(('', UDP_PORT))

# wait for connections on the port. If some are found, send data to them.
# This must be sent as a bytestream, objects don't work here.

# TODO make this with a configurable delay period
print(f"Deploying Server on {UDP_IP}:{UDP_PORT}")
counter = 0
# get the time since the server started


while True:
    d = conn.recvfrom(1024)
    data = d[0]
    addr = d[1]
    counter += 1
    delta = time.time_ns()
    timestamp_msg = str(counter) + " " + str(delta)
    conn.sendto(str.encode(timestamp_msg), addr)
    time.sleep(1)

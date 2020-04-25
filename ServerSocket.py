import socket
import time

# test variables
MESSAGE = "Hello World!"
UDP_PORT = 10000
UDP_IP = "127.0.0.1"  # use the localhost loopback for now

# establish socket object. SOCK_DGRAM indicates a UDP data frame, stored in a static context.
conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# wait for connections on the port. If some are found, send data to them.
# This must be sent as a bytestream, objects don't work here.

# TODO make this with a configurable delay period
print("Deploying Server...")
counter = 0
# get the time since the server started
while True:
    counter += 1
    delta = time.time_ns()
    data = str(counter) + " " + str(delta)
    conn.sendto(str.encode(data), (UDP_IP, UDP_PORT))

    time.sleep(1)

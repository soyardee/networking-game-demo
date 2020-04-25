import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 10000

client_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_conn.bind((UDP_IP, UDP_PORT))

print("Listening...")
# TODO do this with a configurable delay period
while True:
    encode_string = ""
    data = client_conn.recvfrom(1024)
    print(data[0].decode())

    #TODO add timeout after no received messages
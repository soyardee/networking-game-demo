import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = "127.0.0.1"
        self.port = 1234
        self.server_addr = (self.server, self.port)
        self.player = self.connect()

    # init a connection to the server
    def connect(self):
        try:
            return self.client.recvfrom(2048).decode()
        except socket.error:
            print(socket.error)

    # send player information to the server, return a new player state.
    def send(self, data):
        try:
            self.client.sendto(pickle.dumps(data), self.server_addr)
            return pickle.loads(self.client.recvfrom(2048))
        except socket.error:
            print(socket.error)

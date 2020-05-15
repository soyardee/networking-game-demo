import socket
import pickle
from Player import Player


class Network:
    def __init__(self, server_ip, server_port):
        self.state = []
        self.player_id = 0
        self.player = None
        self.players = []
        self.ready = False
        self.connection_status = "connecting"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = server_ip
        self.port = int(server_port)
        self.server_addr = (self.server, self.port)
        self.MAX_DGRAM_SIZE = 4096

    # init a connection to the server
    def connect(self):
        payload = {
            "status": self.connection_status
        }
        try:
            self.socket.sendto(pickle.dumps(payload), self.server_addr)
            data = pickle.loads(self.socket.recvfrom(self.MAX_DGRAM_SIZE)[0])
            self.process_payload(data)
        except socket.error:
            print(socket.error)

    def disconnect(self):
        self.connection_status = "disconnect"
        self.ready = False
        print(f"{self.player_id} initiated disconnect")
        self.send({"status": "disconnect"})
        return

    # send player information to the server, return a new player state.
    # only works when connected to the server.
    def send(self, data):
        try:
            self.socket.sendto(pickle.dumps(data), self.server_addr)
            self.process_payload(pickle.loads(self.socket.recvfrom(self.MAX_DGRAM_SIZE)[0]))
        except socket.error:
            print(socket.error)

    def process_payload(self, payload):
        if payload.get("status") == "max_connection":
            print("server full, cannot connect")
            return
        elif payload.get("status") == "connected" and self.connection_status == "connecting":
            self.connection_status = "connected"
            if not self.ready:
                self.player_id = int(payload.get("player_id"))
                print(f"player id: {self.player_id}")
                self.players = payload.get("player_states")
                self.player = self.players[self.player_id]
                self.ready = True
                return
        elif payload.get("status") == "connected":
            self.players = payload.get("player_states")

    def move(self, direction):
        payload = {
            "status": "connected",
            "command": direction
        }
        self.send(payload)

    def get_players(self):
        return self.players


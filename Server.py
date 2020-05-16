import socket
import pickle
from _thread import *
from Player import Player
import random

MAX_CLIENTS = 4
GAME_SIZE = (1000, 1000)

server = "192.168.1.124"    # localhost binding is fine
port = 9652
# use the UDP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# reserve the port on the machine so that this server is not interrupted
try:
    s.bind((server, port))
# if another instance is present, error and quit
except socket.error as e:
    str(e)


players = []
# list of active clients
clients_addr = []

print("server init complete. waiting for connection...")


# main loop to accept connections
def incoming_conn_listener():
    while True:
        # "entry point" for all incoming requests
        data, addr = s.recvfrom(4096)
        client_status = pickle.loads(data)

        if type(client_status) is dict:
            process_payload(client_status, addr)


def process_state(command, player_id):
    players[player_id].move(command, GAME_SIZE)


def process_payload(data, addr):
    if len(clients_addr) >= MAX_CLIENTS:
        limit_message = {"status": "max_connection"}
        s.sendto(pickle.dumps(limit_message), addr)
        return

    if addr not in clients_addr:
        status = data.get("status")
        if status == "connecting":
            s.sendto(pickle.dumps({"status": "establishing"}), addr)
        elif status == "validated":
            establish_connection(data, addr)
        return

    if data.get("status") == "disconnect":
        leaving = clients_addr.index(addr)
        print(f"player {leaving} initiated disconnect")
        # NOT thread-safe, but this is a single threaded server.
        clients_addr.pop(leaving)
        players.pop(leaving)

        payload = {
            "status": "disconnected"
        }

        s.sendto(pickle.dumps(payload), addr)
        return

    else:
        player_id = clients_addr.index(addr)
        process_state(data.get("command"), player_id)

        payload = {
            "status": "connected",
            "player_id": player_id,
            "player_states": players
        }

        s.sendto(pickle.dumps(payload), addr)


# if the client responds with 'validated', then they are a real client connection
def establish_connection(data, addr):
    clients_addr.append(addr)
    player_id = clients_addr.index(addr)
    players.insert(player_id, Player(50, 50, 30, 30, get_color(player_id)))

    payload = {
        "status": "connected",
        "player_id": player_id,
        "player_states": players
    }

    print(f"{addr} connected as player {player_id}")
    s.sendto(pickle.dumps(payload), addr)
    return


def get_color(index):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
    return colors[index]


incoming_conn_listener()

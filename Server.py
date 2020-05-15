import socket
import pickle
from Player import Player

MAX_CLIENTS = 4
GAME_SIZE = (1000, 1000)

server = "127.0.0.1"    # localhost server is fine
port = 1234
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
        if len(clients_addr) >= MAX_CLIENTS:
            limit_message = {"status": "max_connection"}
            s.sendto(pickle.dumps(limit_message), addr)
            continue

        if addr not in clients_addr:
            clients_addr.append(addr)
            player_id = clients_addr.index(addr)
            players.insert(player_id, Player(50, 50, 30, 30, (255, 0, 255)))

            payload = {
                "status": "connected",
                "player_id": player_id,
                "player_states": players
            }

            print(f"{addr} connected as player {player_id}")
            s.sendto(pickle.dumps(payload), addr)
            continue

        if client_status.get("status") == "disconnect":
            leaving = clients_addr.index(addr)
            print(f"player {leaving} initiated disconnect")
            # NOT thread-safe, but this is a single threaded server.
            clients_addr.pop(leaving)
            players.pop(leaving)

            payload = {
                "status": "disconnected"
            }

            s.sendto(pickle.dumps(payload), addr)
            continue

        else:
            player_id = clients_addr.index(addr)
            process_state(client_status.get("command"), player_id)

            payload = {
                "status": "connected",
                "player_id": player_id,
                "player_states": players
            }

            s.sendto(pickle.dumps(payload), addr)


def process_state(command, player_id):
    players[player_id].move(command, GAME_SIZE)


incoming_conn_listener()

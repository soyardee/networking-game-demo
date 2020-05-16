import socket
import pickle
import threading
import time
from Player import Player

MAX_CLIENTS = 4
GAME_SIZE = (1000, 1000)
TIMEOUT_SECONDS = 4         # how many seconds to wait before a connection is considered dead

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


# locked lists, must yield to a thread before processing.
players = [None, None, None, None]
clients_addr = [None, None, None, None]
clients_time = [None, None, None, None]
total_players = 0

# so that the player state is processed by one thread at a time
state_lock = threading.Lock()


# main loop to accept connections
def incoming_conn_listener():
    while True:
        # "entry point" for all incoming requests
        data, addr = s.recvfrom(4096)
        client_status = pickle.loads(data)

        if type(client_status) is dict:
            process_payload(client_status, addr)


def process_payload(data, addr):
    if total_players >= MAX_CLIENTS:
        limit_message = {"status": "max_connection"}
        s.sendto(pickle.dumps(limit_message), addr)
        return

    status = data.get("status")
    if addr not in clients_addr:
        if status == "connecting":
            s.sendto(pickle.dumps({"status": "establishing"}), addr)
        elif status == "validated":
            establish_connection(data, addr)
        return

    if status == "disconnect":
        state_lock.acquire()
        disconnect(addr)
        state_lock.release()
        return

    player_id = int(clients_addr.index(addr))
    process_state(data.get("command"), player_id)

    payload = {
        "status": "connected",
        "player_id": player_id,
        "player_states": filter_players(players)
    }
    s.sendto(pickle.dumps(payload), addr)

    # mark the last time seen in the client, to be compared by the timeout thread
    clients_time[player_id] = time.time_ns()


def process_state(command, player_id):
    state_lock.acquire(blocking=True)
    players[player_id].move(command, GAME_SIZE)
    state_lock.release()


# if the client responds with 'validated', then they are a real client connection
def establish_connection(data, addr):
    state_lock.acquire()
    player_pos = get_open_slot()
    clients_addr[player_pos] = (addr)
    player_id = player_pos
    players[player_pos] = Player(50, 50, 30, 30, get_color(player_id))
    clients_time[player_pos] = time.time_ns()
    global total_players
    total_players += 1
    state_lock.release()

    payload = {
        "status": "connected",
        "player_id": player_id,
        "player_states": filter_players(players)
    }

    print(f"{addr} connected as player {player_id}")
    s.sendto(pickle.dumps(payload), addr)
    return


# remove the player from the server state
def disconnect(addr):
    index = clients_addr.index(addr)
    print(f"player {index} initiated disconnect")
    clients_addr[index] = None
    players[index] = None
    clients_time[index] = None
    global total_players
    total_players -= 1


# check the player states, if they are not locked every so often.
# feel free to run this once every few seconds. This speeds up server performance.
def check_timeout():
    while True:
        state_lock.acquire()
        current = time.time_ns()
        for i in range(len(clients_time)):
            if clients_time[i] is not None:
                if current - clients_time[i] > TIMEOUT_SECONDS * 1000000000:
                    print(f"connection timeout: {clients_addr[i]}")
                    disconnect(clients_addr[i])
        state_lock.release()
        time.sleep(TIMEOUT_SECONDS)


# get a predefined color for each player based on id
def get_color(index):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
    return colors[index]

def get_open_slot():
    return clients_addr.index(None)


# remove the None values from the player list to send to the clients
def filter_players(player_list):
    return list(filter(None, player_list))


def main():
    timeout_thread = threading.Thread(target=check_timeout, daemon=True)
    timeout_thread.start()

    print("server init complete. waiting for connection...")

    # blocking method, only stops when the kill command is given.
    incoming_conn_listener()


main()

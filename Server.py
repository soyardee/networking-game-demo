import socket
from _thread import *
import pickle

server = "127.0.0.1"    # localhost server is fine
port = 1234
# use the UDP protocol
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# reserve the port on the machine so that this server is not interrupted
try:
    sock.bind((server, port))
# if another instance is present, error and quit
except socket.error as e:
    str(e)

# list of active sessions
sessions = []

"""
    conn: the connection information to the client (where to send and receive input)
    session: the game session
"""

def client_stream(conn, session):
    # send initial state to the adapter when first connecting
    conn.sendto()
    while True:
        try:
            inbound_data = conn.recvfrom(2048)
            if not inbound_data: break

        # if the connection fails, assume the connection is dead
        except:
            break


sock.listen(2)
print("server init complete. waiting for connection...")

# main loop to accept connections
def incoming_conn_listener():
    while True:
        # blocking event, so the loop pauses here until a new connection is received
        conn, addr = sock.accept()
        print(f"New connection discovered: {addr}")
        # start a new thread to handle all player connection information from here
        start_new_thread(client_stream, (conn, ))


def create_session():
    return

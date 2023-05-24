from db import MovieDatabase
import threading
import socket
import struct

class Client:
    def __init__(self, conn, addr):
        self.addr = addr
        self.conn = conn
        self.handle()
        self.conn.close()
    
    def handle(self):
        while True:
            command = struct.unpack('B', self.conn.recv(1))[0]
            if not command: break

            # Create
            if command == 1:
                pass

            # Read
            elif command == 2:
                pass

            # Update
            elif command == 3:
                pass

            # Delete
            elif command == 4:
                pass

            # Listagem de filmes por ator
            elif command == 5:
                pass

            # Listagem de filmes por categoria
            elif command == 6:
                pass

def handleClient(conn, addr):
    Client(conn, addr)

"""
#msg = "bom dia servidor."
person = addressbook_pb2.Person()
person.id = 234
person.name = "Rodrigo Campiolo"
person.email = "rcampiolo@ibest.com.br"

# marshalling
msg = person.SerializeToString()
size = len(msg)
"""

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('127.0.0.1', 5555))
socket.listen()

moviedb = MovieDatabase()

while True:
    conn, addr = socket.accept()
    client = threading.thread(target=handleClient, args=(conn, addr))
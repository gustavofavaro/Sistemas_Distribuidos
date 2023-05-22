from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import threading
import socket
import struct

# Tratar erros
class Database:
    def __init__(self):
        uri = open('uri.env', 'r').read()
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['sample-mflix']

    def insert(self, key, data):
        # Exemplo de data como um dict: {"name" : "John", "address" : "Rua de sla oq"}
        self.db[key].insert_one(data)

    def query(self, key, data):
        return self.db[key].find(data)

    def update(self, key, data, new_data):
        old_data = self.query(key, data)
        if len(old_data) > 1:
            self.db[key].update_many(old_data, new_data)
        else:
            self.db[key].update_one(old_data, new_data)

    def remove(self, key, data):
        to_delete = self.query(key, data)
        if len(to_delete) > 1:
            self.db[key].delete_many(to_delete)
        else:
            self.db[key].delete_one(to_delete)

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

while True:
    conn, addr = socket.accept()
    client = threading.thread(target=handleClient, args=(conn, addr))
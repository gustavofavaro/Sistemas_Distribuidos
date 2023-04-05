import threading
import socket
import struct

ADDR, PORT = '127.0.0.1', 55555

def handle():
    # recebe a mensagem recebida

    # tratar os dados de acordo com a estrutura

    # envia a mensagem recebida

    # (provavelmente guardar os endereços pra enviar pra todo mundo :p)
    pass

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ADDR, PORT))
    
    while True:
        data, addr = sock.recvfrom(1024)
        handle(data, addr)

if __name__ == '__main__':
    main()
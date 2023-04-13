import socket
import struct

ADDR, PORT = '127.0.0.1', 55555

def handle():
    pass

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    teste = 'teste do client'
    
    sock.sendto(teste.encode('utf-8'), ADDR, PORT)

if __name__ == '__main__':
    main()
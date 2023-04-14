import socket
import threading
import struct

ADDR, PORT = '127.0.0.1', 55555

def handle_recv(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024) # addr a gente usa para distinguir?
            print(data.decode('utf-8'))
            
        except Exception as e:
            print(f'Erro: {e}')

def handle_send(sock):
    while True:
        try:
            data = input()
            if data == 'EXIT':
                sock.close()
                break
            sock.sendto(data.encode('utf-8'), (ADDR, PORT))

        except Exception as e:
            print(f'Erro: {e}')

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    threading.Thread(target = handle_recv, args = (sock)).start()
    threading.Thread(target = handle_send, args = (sock)).start()

if __name__ == '__main__':
    main()
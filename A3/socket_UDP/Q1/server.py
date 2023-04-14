import threading
import socket
import struct

ADDR, PORT = '127.0.0.1', 55555

def handle_recv(sock, data, addr):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except Exception as e:
            print(f'Erro: {e}')
    

    # recebe a mensagem recebida

    # tratar os dados de acordo com a estrutura

    # envia a mensagem recebida

    # (provavelmente guardar os endereços pra enviar pra todo mundo :p)

def handle_send(sock):
    pass

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind((ADDR, PORT))
        threading.Thread(target = handle_recv, args = (sock)).start()
        threading.Thread(target = handle_send, args = (sock)).start()

    except Exception as e:
        print(f'Erro: {e}')
    

if __name__ == '__main__':
    main()


# - tipo de mensagem [1 byte]
# - tamanho apelido (tam_apl) [1 byte]
# - apelido [tam_apl (1 a 64) bytes ]
# - tamanho mensagem (tam_msg) [1 byte]
# - mensagem [tam_msg bytes]

# Os tipos de mensagem são:
# 1: mensagem normal
# 2: emoji
# 3: URL
# 4: ECHO (envia e recebe a mesma mensagem para indicar que usuário está ativo).
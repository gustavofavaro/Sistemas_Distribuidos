import threading
import socket
import struct

ADDR, PORT = '127.0.0.1', 55555

def handle_recv(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f'Usuário com ip {addr[0]}:{addr[1]} enviou mensagem.')
        except Exception as e:
            print(f'Erro: {e}')
    

    # recebe a mensagem recebida

    # tratar os dados de acordo com a estrutura

    # envia a mensagem recebida

    # (provavelmente guardar os endereços pra enviar pra todo mundo :p)

def handle_send(sock):
    # while True:
    #     try:
    #         data = input()
    #         if data == 'EXIT':
    #             sock.close()
    #             break
    #         sock.sendto(data.encode('utf-8'), (ADDR, PORT))

    #     except Exception as e:
    #         print(f'Erro: {e}')
    pass

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind((ADDR, PORT))
        threading.Thread(target = handle_recv, args = (sock,)).start()
        #threading.Thread(target = handle_send, args = (sock,)).start()
        
        while True:
            data = input()
            if data == 'EXIT':
                sock.close()
                break
            sock.sendto(data.encode('utf-8'), (ADDR, PORT))

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
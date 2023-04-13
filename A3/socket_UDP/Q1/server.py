import threading
import socket
import struct

ADDR, PORT = '127.0.0.1', 55555

def handle(data, addr):

    print(f'Mensagem do cliente: {data}')
    teste = "teste"
    sock.sendto(teste.encode('utf-8'), addr)
    # recebe a mensagem recebida

    # tratar os dados de acordo com a estrutura

    # envia a mensagem recebida

    # (provavelmente guardar os endereços pra enviar pra todo mundo :p)
    pass

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind((ADDR, PORT))
        while True:
            data, addr = sock.recvfrom(1024)
            handle(data, addr)

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
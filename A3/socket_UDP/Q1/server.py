import threading
import socket
import struct
class Server:
    def __init__(self, nickname, addr, port):
        self.nickname = nickname
        self.address = (addr, port)

        self.connected_users = []
        self.is_open = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)

        self.is_open = True
        threading.Thread(target = self.handle_recv, args = (self.sock,)).start()
        threading.Thread(target = self.handle_send, args = (self.sock,)).start()

    # Envia a mensagem para os clientes conectados que são conhecidos
    def send_to_connected_users(self, message):
        for user in self.connected_users:
            self.sock.sendto(message, user[1])

    def handle_recv(self, sock):
        while self.is_open:
            try:
                # Recebe a mensagem de algum cliente conectado ao servidor
                data, addr = sock.recvfrom(323) # 1 + 1 + 64 + 1 + 255

                # Separa as partes do pacote recebido
                message_type, nickname_size = struct.unpack('BB', data[0:2])
                nickname = data[2:2+nickname_size].decode('utf-8')
                message_size = struct.unpack(data[2+nickname_size:3+nickname_size])
                message = (data[3+nickname_size:3+nickname_size+message_size]).decode('utf-8')

                # Adicionar apelido e endereço na lista de usuários conectados na primeira mensagem
                if (nickname, addr) not in self.connected_users:
                    self.connected_users.append((nickname, addr))

                # Mensagem normal ou emoji (as duas mensagens são formato utf-8)
                if message_type == 1 or message_type == 2:
                    print(f'{nickname}: {message}')

                # Mensagem é uma URL
                elif message_type == 3:
                    print(f'{nickname} mandou a URL: {message}') 

                # Mensagem é um echo
                elif message_type == 4:
                    print(f"ECHO: {message}")

                # Monta o pacote da mensagem recebida e a envia para os outros clientes
                message_pack = struct.pack(
                    f'BB{nickname_size}sB{message_size}s',
                    message_type,
                    nickname_size,
                    nickname,
                    message_size,
                    message
                )
                
                if message_type != 4:
                    self.send_to_connected_users(message_pack)
                else:
                    self.sock.sendto(message_pack, addr)

            except Exception as e:
                print(f'Erro: {e}')

    def handle_send(self):
        while True:
            try:
                message = input('> ')
                if message == 'EXIT':
                    self.is_open = False
                    break

                # Categoriza o tipo da mensagem

                # Se a mensagem é um emoji
                if message[0] == ':' and message[-1] == ':' and ' ' not in message:
                    message_type = 2
                    # Transforma a mensagem em emoji unicode
                
                # Se a mensagem é um link
                elif '://' in message and ' ' not in message:
                    message_type = 3

                # Se a mensagem for um echo
                elif message[0:3] == 'echo':
                    echo, destination = message.split(' ', 1)
                    # sendto('echo', destination)
                    message_type = 4
                
                # Caso não se enquadre, mensagem é apenas normal
                else:
                    message_type = 1
                

                # Codifica tudo
                message_pack = struct.pack(
                    f'BB{len(self.nickname)}sB{len(message)}s',
                    message_type,
                    len(self.nickname),
                    self.nickname,
                    len(message),
                    message
                )
                self.send_to_connected_users(message_pack)

            except Exception as e:
                print(f'Erro: {e}')

nickname = input("Insira o seu nickname: ")
addr = input("Insira seu endereço de IP: ")
port = input("Insira sua porta: ")
sv = Server(nickname, addr, port)

# recebe a mensagem recebida
# tratar os dados de acordo com a estrutura
# envia a mensagem recebida
# (provavelmente guardar os endereços pra enviar pra todo mundo :p)

# - tipo de mensagem [1 byte]
# - tamanho apelido (tam_apl) [1 byte]
# - apelido [tam_apl (1 a 64) bytes ]
# - tamanho mensagem (tam_msg) [1 byte]
# - mensagem [tam_msg bytes]

# Os tipos de mensagem são:
# 1: mensagem normal 0x00
# 2: emoji 0x01
# 3: URL 0x02
# 4: ECHO (envia e recebe a mesma mensagem para indicar que usuário está ativo). 0x03
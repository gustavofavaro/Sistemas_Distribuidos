import threading
import socket
import struct
import unicodedata
class Server:
    def __init__(self, nickname, addr, port):
        self.nickname = nickname
        self.address = (addr, port)
        self.connected_users = []
        self.receiver = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)
        self.emoji_dict = {
            "brand": "Ford",
            "model": "Mustang",
            "year": 1964
        }

        self.is_open = True
        threading.Thread(target = self.handle_recv).start()
        threading.Thread(target = self.handle_send).start()

    # Envia a mensagem para os clientes conectados que são conhecidos, exceto pelo que enviou a mensagem
    def send_to_connected_users(self, message, sender_addr):
        for user in self.connected_users:
            if sender_addr == user[1]: continue
            self.sock.sendto(message, user[1])

    def handle_recv(self):
        while self.is_open:
#            try:
                # Recebe a mensagem de algum cliente conectado ao servidor
                data, addr = self.sock.recvfrom(323) # 1 + 1 + 64 + 1 + 255 + 1 (addr)

                # Separa as partes do pacote recebido
                message_type, nickname_size = struct.unpack('BB', data[0:2])
                nickname = data[2:2+nickname_size].decode('utf-8')
                message_size, = struct.unpack('B', data[2+nickname_size:3+nickname_size])
                message = data[3+nickname_size:3+nickname_size+message_size].decode('utf-8')

                # Verificação de saída
                if message_type == 7 and addr == self.address:
                    break

                # Mensagem normal ou emoji (as duas mensagens são formato utf-8)
                if message_type == 1:
                    print(f'{nickname}: {message}')

                elif message_type == 2:
                    #emoji = message.strip(":")
                    print(f'{nickname}:{unicodedata.lookup(message[1:-1])}')
                    #print('%s: \N{%s}' % (nickname, message))

                # Mensagem é uma URL
                elif message_type == 3:
                    print(f'{nickname} mandou a URL: {message}') 

                # Mensagem é um echo
                elif message_type == 4:
                    # Trata a resposta e finaliza a operação
                    if message == 'rply':
                        print(f'ECHO reply de {nickname}.')
                        continue

                    # Recebe a requisição e manda a resposta
                    print(f"ECHO request de {nickname}: {message}")
                    message = 'rply'

                # Mensagem é um sinal de conexão
                elif message_type == 5:
                    if (nickname, addr) not in self.connected_users:
                        self.connected_users.append((nickname, addr))
                
                # Mensagem é um sinal de desconexão
                elif message_type == 6:
                    if (nickname, addr) not in self.connected_users:
                        continue
                    self.connected_users.remove((nickname, addr))

                # Monta o pacote da mensagem recebida e a envia para os outros clientes
                message_pack = struct.pack(
                    f'BB{nickname_size}sB{message_size}s',
                    message_type,
                    nickname_size,
                    bytes(nickname, 'utf-8'),
                    message_size,
                    bytes(message, 'utf-8')
                )
                
                if message_type == 4 and message == 'rply':
                    self.sock.sendto(message_pack, addr)
                else:
                    self.send_to_connected_users(message_pack, addr)

#            except Exception as e:
#                print(f'Erro: {e}')

    def handle_send(self):
        while True:
#            try:
                entire_message = input('> ')
                message, *args = entire_message.split(' ', 1)
                if message == 'EXIT':
                    self.is_open = False
                    message_pack = struct.pack(
                        f'BB{len(self.nickname)}sB{len(message)}s',
                        7,
                        len(self.nickname),
                        bytes(self.nickname, 'utf-8'),
                        len(message),
                        bytes(message, 'utf-8')
                    )
                    self.sock.sendto(message_pack, self.address)
                    break

                # Identifica comandos especificos
                if message == 'ECHO':
                    message_type = 4
                
                # Setter para determinar o cliente p2p destinatário
                elif message == 'CONNECT':
                    message_type = 5
                    addr, port = args[0].split(':')
                    self.receiver = (addr, int(port))
                
                # Sinal de desconexão para parar de receber mensagens de um cliente p2p
                elif message == 'DISCONNECT':
                    if args[0] != self.receiver:
                        raise Exception('Endereço dado é diferente do receptor settado para este cliente.')
                    message_type = 6

                # Se a mensagem é um emoji
                elif entire_message[0] == ':' and entire_message[-1] == ':':
                    message_type = 2
                    message = entire_message
                    # Transforma a mensagem em emoji unicode
                
                # Se a mensagem é um link
                elif '://' in message:
                    message_type = 3

                # Caso não se enquadre, mensagem é apenas normal
                else:
                    message_type = 1
                    message = entire_message

                # Codifica tudo
                message_pack = struct.pack(
                    f'BB{len(self.nickname)}sB{len(message)}s',
                    message_type,
                    len(self.nickname),
                    bytes(self.nickname, 'utf-8'),
                    len(message),
                    bytes(message, 'utf-8')
                )
                if not self.connected_users:
                     # Verifica se há um destinatário setado
                    if not self.receiver:
                        raise Exception('Este cliente não possui um destinatário setado e nem usuários conectados. Você pode setar utilizando o comando CONNECT <endereço_ip><port>.')   
                    self.sock.sendto(message_pack, self.receiver)
                else:
                    self.sock.sendto(message_pack, self.connected_users[0][1])

                # Após enviar o pacote, verifica se o comando foi de desconexão
                if message_type == 6:
                    self.receiver = None

#            except Exception as e:
#                pass
#                #print(f'Erro: {e}')

nickname = input("Insira o seu nickname: ")
addr = input("Insira seu endereço de IP: ")
port = input("Insira sua porta: ")
sv = Server(nickname, addr, int(port))

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
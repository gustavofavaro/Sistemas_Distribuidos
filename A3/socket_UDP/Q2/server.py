#!/usr/bin/env python3
#-----------------------------------------------------------------------
# Autores: Fabricio Flávio Martins Damasceno e Gustavo Sengling Favaro
# Data de criação: 18/04/2023
# Data da última atualização: 18/04/2023
#-----------------------------------------------------------------------
""" Implementação do servidor da atividade de socket UDP Questão 2 utilizando socket UDP """
#-----------------------------------------------------------------------


import threading
import socket
import struct
import psutil # pip install psutil (pega o espaço em disco do pc)
import platform # pega o SO do pc
import hashlib
import os

class Server:
    def __init__(self, addr, port):
        self.address = (addr, port)
        self.address_uploading = None
        self.file = None
        self.filename = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)

        threading.Thread(target = self.handle).start()

    def handle(self):
        while True:
    #        try:
                # Recebe a mensagem de algum cliente conectado ao servidor
                # Primeiro byte: Tipos de mensagem / 1: Requisição / 2: Resposta
                # Segundo byte: Comandos / 1: Request de upload + dados do arquivo / 2: Partes do upload / 3: fim de upload
                data, addr = self.sock.recvfrom(2048)
                message_type, command = struct.unpack('BB', data[0:2])
                if message_type != 1:
                    continue

                # Request de upload
                if command == 1:
                    # Recebe os dados do arquivo
                    filename_size, = struct.unpack('B', data[2:3])
                    filename = data[3:(3+filename_size)].decode('utf-8')
                    file_size, = struct.unpack('!I', data[(3+filename_size):(3+filename_size+4)])

                    print(f'Arquivo {filename} com tamanho {file_size/1024}kB a ser enviado de {addr[0]}:{addr[1]}')

                    # Seta o path do disco de acordo com o sistema operacional
                    if platform.system() == 'Windows':
                        path = 'C:/'
                    else:
                        path = '/'

                    # Verifica o espaço em disco e compara com o tamanho do arquivo
                    free_disk_space = psutil.disk_usage(path).free   
                    if free_disk_space > file_size:
                        result = 1
                    else:
                        result = 2

                    # Resposta da solicitação do servidor
                    response = struct.pack(
                        'BBB',
                        2,          # Resposta
                        command,    # Comando
                        result      # Sucesso ou fracasso
                    )
                    self.sock.sendto(response, addr)

                    self.file = open(f'./server_files/{filename}', 'ab')
                    self.address_uploading = addr
                    self.filename = filename

                # Partes do upload
                elif command == 2:
                    # os códigos hash SHA-1 sempre vão possuir 20 caracteres 
                    hash_from_client_len, = struct.unpack('B', data[2:3])
                    hash_from_client = data[3:(3+hash_from_client_len)]
                    data_chunk_len, = struct.unpack('!I', data[(3+hash_from_client_len):(7+hash_from_client_len)])
                    data_chunk = data[(7+hash_from_client_len):(7+hash_from_client_len+data_chunk_len)]
                    hash_from_server = hashlib.sha1(data_chunk).digest()

                    #print('chunk')
                    #print(hash_from_server)
                    #print(hash_from_client)

                    if hash_from_server != hash_from_client:
                        result = 2
                        print('n passou\n')
                    else:
                        self.file.write(data_chunk)
                        result = 1
                
                    response = struct.pack(
                        'BBB',
                        2,          # Resposta
                        command,    # Comando
                        result      # Sucesso ou fracasso
                    )

                    self.sock.sendto(response, addr)
                
                elif command == 3:
                    # recebe o hash do arquivo inteiro e compara com o que o servidor recebeu
                    # responde sucesso ou falha pela comparação de hash, se falhou apagar o arquivo enviado
                    hash_from_client_len, = struct.unpack('B', data[2:3])
                    hash_from_client = data[3:(3+hash_from_client_len)]

                    self.file.close()
                    self.file = open(f'./server_files/{filename}', 'rb')
                    file_data = self.file.read()
                    hash_from_server = hashlib.sha1(file_data).digest()

                    print('final')
                    print(hash_from_server)
                    print(hash_from_client)

                    if hash_from_client != hash_from_server:
                        result = 2
                        self.file.close()
                        # os.remove(f'./server_files/{self.filename}')
                    else:
                        result = 1
                        self.file.close()
                    

                    self.address_uploading = None
                    self.filename = None
                    
                response = struct.pack(
                    'BBB',
                    2,          # Resposta
                    command,    # Comando
                    result      # Sucesso ou fracasso
                )

                self.sock.sendto(response, addr)

    #        except Exception as e:
#            print(f'Erro: {e}')

sv = Server('127.0.0.1', 5555)
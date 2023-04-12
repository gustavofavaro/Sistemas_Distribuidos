#!/usr/bin/env python3
#-----------------------------------------------------------------------
# Autores: Fabricio Flávio Martins Damasceno e Gustavo Sengling Favaro
# Data de criação: 03/04/2023
# Data da última atualização: 11/04/2023
#-----------------------------------------------------------------------
""" Implementação do cliente da atividade de socket TCP Questão 2 utilizando socket TCP """
#-----------------------------------------------------------------------

import threading
import socket
import struct
import os
import logging

ADDR, PORT = '127.0.0.1', 55555

def handle(conn, addr):
    try:
        while True:
            # Recebe os três primeiros dados da mensagem
            message_info = conn.recv(3)

            # Verifica se não vieram dados para desconectar o usuário e registrar no log 
            if not message_info:
                conn.close()
                break

            # Desempacota os três dados
            type, command, filename_size = struct.unpack('BBB', message_info)

            # Ignora a mensagem caso ela não seja uma requisição
            if type != 1: continue

            # Recebe o nome do arquivo dado o tamanho recebido anteriormente
            # o comando GETFILESLIST não inclui nome do arquivo.
            if command != 3:
                filename = conn.recv(filename_size).decode('utf-8')

            # ADDFILE: adiciona um arquivo novo.
            if command == 1:
                try:
                    # Verificando se o nome do arquivo é válido
                    if filename == '':
                        raise Exception('Nome de arquivo inválido.')

                    # Logging
                    logging.info(f'Usuário {addr[0]}:{addr[1]} adicionando arquivo {filename} ao servidor.')

                    # Recebe o tamanho do arquivo
                    file_size_bytes = conn.recv(4)
                    file_size, = struct.unpack('!I', file_size_bytes) # ! = big-endian

                    # Cria o arquivo no diretório do servidor
                    file = open(f'./server_files/{filename}', 'ab')

                    # Recebe cada byte e grava no arquivo
                    for _ in range(file_size):
                        file.write(bytes(conn.recv(1)))
                    
                    # Fecha o arquivo e marca operação como bem sucedida
                    file.close()
                    logging.info(f'Arquivo {filename} adicionado ao servidor.')   
                    result = 1

                except Exception as e:
                    logging.info(f'Erro no ADDFILE: {e}.')
                    result = 2

                # Estrutura da resposta
                response = struct.pack(
                        'BBB',      # três inteiros
                        1,          # código de resposta
                        2,          # código do comando
                        result      # código de sucesso
                    )
                conn.send(response)
            
            # DELETE: remove um arquivo existente.
            elif command == 2:
                try:
                    # Verificando se o nome do arquivo é válido
                    if filename == '':
                        raise Exception('Nome de arquivo inválido.')
                    
                    # Logging
                    logging.info(f'Usuário {addr[0]}:{addr[1]} removendo o arquivo {filename} do servidor.')

                    # Remove o arquivo do sistema
                    os.remove(f'./server_files/{filename}')
                    logging.info(f'Arquivo {filename} deletado do servidor.')    
                    result = int(1)
                    
                except Exception as e:
                    # Captura um erro na remoção
                    logging.info(f'Erro no DELETE: {e}.')
                    result = int(2)
                
                # Estrutura da resposta
                response = struct.pack(
                        'BBB',      # três inteiros
                        2,          # código de resposta
                        2,          # código do comando
                        result      # código de sucesso
                    )
                conn.send(response)
            
            # GETFILESLIST: retorna uma lista com o nome dos arquivos.
            elif command == 3:
                try:
                    # Logging
                    logging.info(f'Usuário {addr[0]}:{addr[1]} solicitou a lista de arquivos do servidor.')
                    
                    # Recebe a lista de arquivos no diretório
                    file_list = list(filter(os.path.isfile, os.listdir(path='./server_files')))

                except Exception as e:
                    # Captura um erro na construção da lista de arquivos
                    logging.info(f'Erro no GETFILESLIST: {e}.')
                    
                    # Envia a resposta com código de erro
                    response = struct.pack(
                        'BBB',      # três inteiros
                        2,          # código de resposta
                        3,          # código do comando
                        2           # código de erro
                    )
                    conn.send(response)
                    continue

                # Envia a resposta com código de sucesso
                response = struct.pack(
                    'BBBB',         # quatro inteiros
                    2,              # código de resposta
                    3,              # código do comando
                    1,              # código de sucesso
                    len(file_list)  # número de arquivos
                )
                conn.send(response)
                logging.info(f'Sucesso no GETFILESLIST.')
                    
                # Envia os nomes dos arquivos do diretório
                for file in file_list:
                    file_info = struct.pack(
                        f'B{len(file)}s',       # um inteiro e uma cadeia de {len(file)} bytes
                        len(file),              # tamanho do nome do arquivo
                        bytes(file, 'utf-8')    # nome do arquivo em bytes
                    )
                    conn.send(file_info)
                    
            
            # GETFILE: faz download de um arquivo.
            elif command == 4:
                try:
                    # Verificando se o nome do arquivo é válido
                    if filename == '':
                        raise Exception('Nome de arquivo inválido.')
                    
                    # Logging
                    logging.info(f'Usuário {addr[0]}:{addr[1]} baixando o arquivo {filename} do servidor.')

                    file = open(f'./server_files/{filename}', 'rb')
                    file_data = file.read()
                    file.close()

                except Exception as e:
                    # Captura um erro na leitura do arquivo
                    logging.info(f'Erro no GETFILE: {e}.')

                    # Envia a resposta com código de erro
                    response = struct.pack(
                        'BBB',          # três inteiros
                        2,              # código de resposta
                        4,              # código do comando
                        2               # código de erro
                    )
                    conn.send(response)
                    continue

                # Envia a resposta com código de sucesso
                response = struct.pack(
                    '!BBBI',        
                    2,              # código de resposta
                    4,              # código do comando
                    1,              # código de sucesso
                    len(file_data)  # tamanho do arquivo
                )
                conn.send(response)

                for i in range(len(file_data)):
                    conn.send(struct.pack('B', file_data[i]))
        
                logging.info(f'Arquivo {filename} baixado com sucesso.')

        logging.info(f'Conexão com {addr[0]}:{addr[1]} finalizada.')


    except Exception as e:
        logging.info(f'Erro no handle: {e}.')

        logging.info(f'Usuário com endereço {addr[0]}:{addr[1]} desconectou-se.')
        conn.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d/%b/%y %H:%M:%S', level=logging.DEBUG)
    
    try:
        sock.bind((ADDR, PORT))
        sock.listen(10)
        while True:
            conn, addr = sock.accept()
            logging.info(f'Usuário com endereço {addr[0]}:{addr[1]} conectou-se.')
            
            client_thread = threading.Thread(target=handle, args=(conn, addr))
            client_thread.start()
    
    except Exception as e:
        print(f'Erro: {e}')

if __name__ == '__main__':
    main()
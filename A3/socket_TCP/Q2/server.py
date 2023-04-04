from datetime import datetime
from zoneinfo import zoneinfo
import threading
import socket
import struct
import os

ADDR, PORT = '127.0.0.1', 55556

def write_on_log(message):
    timezone = zoneinfo('America/Sao_Paulo')
    datetime_br = datetime.now(timezone)
    current_datetime = datetime_br.strftime("%D - %H:%M:%S")

    log = open('log.txt', 'a')
    log.writelines(f'{current_datetime} -- {message}\n')
    log.close()

def handle(conn, addr):
    try:
        while True:
            # Recebe os três primeiros dados da mensagem
            message_info = conn.recv(3)

            # Verifica se não vieram dados para desconectar o usuário e registrar no log 
            if not message_info:
                conn.close()
                write_on_log(f'Usuário com endereço {addr[0]}:{addr[1]} desconectou-se.')
                break

            # Desempacota os três dados
            type, command, filename_size = struct.unpack('BBB', message_info)

            # Ignora a mensagem caso ela não seja uma requisição
            if type != 1: continue

            # Recebe o nome do arquivo dado o tamanho recebido anteriormente
            filename = conn.recv(filename_size).decode('utf-8')

            # ADDFILE: adiciona um arquivo novo.
            if command == 1:
                try:
                    # Recebe o tamanho do arquivo
                    file_info = conn.recv(4)
                    file_size, = struct.unpack('!I', file_info) # ! = big-endian

                    # Cria o arquivo no diretório do servidor
                    file = open(f'./server_files/{filename}', 'ab')

                    # Recebe cada byte e grava no arquivo
                    for _ in range(file_size):
                        file.write(bytes(conn.recv(1)))
                    
                    # Fecha o arquivo e marca operação como bem sucedida
                    file.close()
                    result = 1

                except Exception as e:
                    write_on_log(f'Erro no ADDFILE: {e}.')
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
                    # Remove o arquivo do sistema
                    os.remove(f'./server_files/{filename}')
                    result = 1
                    
                except:
                    # Captura um erro na remoção
                    write_on_log(f'Erro no DELETE: {e}.')
                    result = 2
                
                # Estrutura da resposta
                response = struct.pack(
                        'BBB',      # três inteiros
                        2,          # código de resposta
                        2,          # código do comando
                        result      # código de sucesso
                    )
                conn.send(response)
            
            # GETFILELIST: retorna uma lista com o nome dos arquivos.
            elif command == 3:
                try:
                    # Recebe a lista de arquivos no diretório
                    file_list = list(filter(os.path.isfile, os.listdir(path='./server_files')))

                except Exception as e:
                    # Captura um erro na construção da lista de arquivos
                    write_on_log(f'Erro no GETFILELIST: {e}.')
                    
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
                    'BBBH',         # quatro inteiros
                    2,              # código de resposta
                    3,              # código do comando
                    1,              # código de sucesso
                    len(file_list)  # número de arquivos
                )
                conn.send(response)

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
                    file = open(f'./server_files/{filename}', 'rb')
                    file_data = file.read()
                    file.close()

                except:
                    # Captura um erro na leitura do arquivo
                    write_on_log(f'Erro no GETFILE: {e}.')

                    # Envia a resposta com código de erro
                    response = struct.pack(
                        'BBB',          # três inteiros
                        2,              # código de resposta
                        4,              # código do comando
                        2               # código de erro
                    )
                    continue

                # Envia a resposta com código de sucesso
                response = struct.pack(
                    'BBBH',         # quatro inteiros
                    2,              # código de resposta
                    4,              # código do comando
                    1,              # código de sucesso
                    len(file_data)  # tamanho do arquivo
                )
                conn.send(response)

                for i in range(len(file_data)):
                    conn.send(file_data[i])


    except Exception as e:
        write_on_log(f'Erro no handle: {e}.')
        write_on_log(f'Usuário com endereço {addr[0]}:{addr[1]} desconectou-se.')
        conn.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind((ADDR, PORT))
        sock.listen(10)
        while True:
            conn, addr = sock.accept()
            write_on_log(f'Usuário com endereço {addr[0]}:{addr[1]} conectou-se.')
            
            client_thread = threading.Thread(target=handle, args=(conn, addr))
            client_thread.start()
    
    except Exception as e:
        print(f'Erro: {e}')

if __name__ == '__main__':
    main()
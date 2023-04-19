#!/usr/bin/env python3
#-----------------------------------------------------------------------
# Autores: Fabricio Flávio Martins Damasceno e Gustavo Sengling Favaro
# Data de criação: 18/04/2023
# Data da última atualização: 18/04/2023
#-----------------------------------------------------------------------
""" Implementação do cliente da atividade de socket UDP Questão 2 utilizando socket UDP """
#-----------------------------------------------------------------------

import socket
import struct
import hashlib
import time

def handle(sock, server_addr):
    while True:
#        try:
            command, *args = input('> ').split(' ')

            if command == 'UPLOAD':
                # Pega o arquivo
                if '/' in args[0]:
                    filename = args[0][-1]
                else:
                    filename = args[0]
                
                file = open(args[0], 'rb')
                file_data = file.read()
                file_hash = hashlib.sha1(file_data).digest()
                file.close()
                file_size = len(file_data)

                # Solicitação de envio
                request = struct.pack(
                    f'!BBB{len(filename)}sI',
                    1,
                    1,
                    len(filename),
                    bytes(filename, 'utf-8'),
                    file_size
                )
                sock.sendto(request, server_addr)

                # Resposta da solicitação de envio
                response, addr = sock.recvfrom(4)
                message_type, command, result = struct.unpack('BBB', response)
                
                if result == 2:
                    raise Exception('Arquivo grande demais para o servidor.')

                if result == 1:
                    file = open(args[0], 'rb')
                    upload_error = False
                    i = file_size
                    while True:
                        if i == 0:
                            break
                        if i < 1024:
                            chunk = i
                            i = 0
                        else:
                            chunk = 1024
                            i -= 1024
                        # Lê os próximos pacotes enquanto não houver erro no envio
                        if not upload_error: 
                            data_chunk = file.read(chunk)

                        # Se não houver pedaço do arquivo, o arquivo foi lido por completo
                        if not data_chunk:
                            break

                        # Obtém o hash do pedaço
                        chunk_hash = hashlib.sha1(data_chunk).digest()

                        # Envio dos pacotes
                        request = struct.pack(
                            'BB20s1024s',
                            1,
                            2,
                            chunk_hash,
                            data_chunk
                        )
                        sock.sendto(request, server_addr)
                        time.sleep(0.01)

                    # Fim do loop, arquivo terminou de ser enviado
                    # Envio do EOF e código hash do arquivo inteiro para verificação

                    print(file_hash)

                    request = struct.pack(
                        'BB20s',
                        1,
                        3,
                        file_hash,
                    )
                    sock.sendto(request, server_addr)
                    
                    # Resultado do envio
                    response, addr = sock.recvfrom(4)
                    message_type, command, result = struct.unpack('BBB', response)

                    if result == 3:
                        raise Exception('Servidor está ocupado, aguarde um momento e tente novamente.')
                    if result == 2:
                        upload_error = True
                    else:
                        upload_error = False
                    
                    
                    # Resultado do envio
                    response, addr = sock.recvfrom(4)
                    message_type, command, result = struct.unpack('BBB', response)

                    if response == 1:
                        print('Arquivo enviado com sucesso.')
                    elif response == 2:
                        raise Exception('Erro no envio do arquivo, tente novamente.')
                    elif response == 3:
                        raise Exception('Servidor está ocupado, aguarde um momento e tente novamente.')
                        
#        except Exception as e:
#            print(f'Erro: {e}.')


def main():
    while True:
        addr, *port = input('Endereço do servidor de upload: ').split(':')
        
        if addr == 'SAIR':
            return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            break

        except Exception as e:
            print(f'Erro na conexão: {e}. Tente novamente.')
            continue
    
    handle(sock, (addr, int(port[0])))

if __name__ == '__main__':
    main()
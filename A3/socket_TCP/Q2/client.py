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

    log = open('client_log.txt', 'a')
    log.writelines(f'{current_datetime} -- {message}\n')
    log.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ADDR, PORT))

    if not sock:
        print('Conexão falhou, tente novamente.')
        return
    
    while True:
        command, *args = input('> ').split(' ', 1)

        if command == 'ADDFILE':
            try:
                file = open(args[0], 'rb')
                file_data = file.read()
                file.close()

                if '/' in args[0]:
                    dirs = args.split('/')
                    filename = dirs[-1]
                else:
                    filename = args[0]

            except Exception as e:
                print('Operação falhou: consulte o log para mais informações.')
                # logging
                continue
            
            # Envia a requisição
            request = struct.pack(
                f'BBH{len(filename)}s',     # quatro inteiros
                1,                          # código de requisição
                1,                          # código do comando
                len(filename),              # tamanho do nome do arquivo
            )
            sock.send(request)

       
            response_info = sock.recv(3)
            type, command, success = struct.unpack('BBB', response_info)
            
            if type != 2: continue
            
            if success == 1:
                print('Deu bom.')

                for i in range(len(file_data)):
                    sock.recv(file_data[i])


                # Logging
            else:
                print('Deu ruim')
                # Logging            
            

        elif command == 'DELETE':
            try:
                request = struct.pack(
                    f'BBH{len(args[0])}s',
                    1,               # código de requisição
                    2,               # código do comando
                    len(args[0]),
                )
                sock.send(request)
                
                response_info = sock.recv(3)
                type, command, success = struct.unpack('BBB', response_info)

                if type != 2: continue
            
                if success == 1:
                    print('Deu bom.')
                    # Logging
                else:
                    print('Deu ruim')
                    # Logging            

            except Exception as e:
                print('Operação falhou: consulte o log para mais informações.')
                # logging
                continue


        elif command == 'GETFILELIST':
            try:
                request = struct.pack(
                    'BB',
                    1,               # código de requisição
                    3               # código do comando
                )
                sock.send(request)
                
                response_info = sock.recv(3)
                type, command, success = struct.unpack('BBB', response_info)

                if type != 2: continue
            
                if success == 1:
                    print('Deu bom.')
                    # Logging

                    file_size = sock.recv(1)

                    for _ in range(int(file_size)):
                        filename_size_bytes = sock.recv(1)
                        filename_size = struct.unpack('B')
                        filename_size, filename = struct.unpack(f'')


                else:
                    print('Deu ruim')
                    # Logging   

                
            except Exception as e:
                print('Operação falhou: consulte o log para mais informações.')
                # logging
                continue


        elif command == 'GETFILE':
            try:
                request = struct.pack(
                    f'BBH{len(args[0])}s',
                    1,               # código de requisição
                    4,               # código do comando
                    len(args[0]),
                )
                sock.send(request)

                response_info = sock.recv(3)
                type, command, success = struct.unpack('BBB', response_info)
                
                if type != 2: continue
                

                if success == 1:
                    print('Deu bom.')
                    # Logging

                    file_size = sock.recv(1)

                    file = open(args[0], 'ab')

                    for i in range(len(file_size)):
                        file.write(i)
                    
                    file.close()
                    
                else:
                    print('Deu ruim')
                    # Logging      
                
            except Exception as e:
                print('Operação falhou: consulte o log para mais informações.')
                # logging
                continue

        elif command == 'EXIT': 
            sock.close()
            break

if __name__ == '__main__':
    main()

    # Issues:
    # Cabeçalho
    # Comentários
    # Organizar (funções no handle)
    # getfilelist
    # revisar os comando
import socket
import struct
import sys

ADDR, PORT = '127.0.0.1', 55555

def handle(sock):
    while True:
        command, *args = input('> ').split(' ', 1)

        # ADDFILE: adiciona um arquivo ao servidor.
        if command == 'ADDFILE':
            # Abertura do arquivo e leitura de dados.
            try:
                file = open(args[0], 'rb')
                file_data = file.read()
                file.close()
                
                if '/' in args[0]:
                    dirs = args[0].split('/')
                    filename = dirs[-1]
                else:
                    filename = args[0]

            # Ignora a operação e informa o erro na abertura do arquivo.
            except Exception as e:
                print(f'Erro: {e}.')
                continue

            # Envia a requisição.
            request = struct.pack(
                f'!BBB{len(filename)}sI',
                1,                          # código de requisição
                1,                          # código do comando
                len(filename),              # tamanho do nome do arquivo
                bytes(filename, 'utf-8'),   # nome do arquivo
                len(file_data)              # tamanho do arquivo
            )
            sock.send(request)

            # Envia o arquivo byte a byte
            print(f'Tamanho do arquivo: {len(file_data)}')
            for i in range(len(file_data)):
                sock.send(struct.pack('B', file_data[i]))
       
            # Recebe a resposta do servidor.
            response_info = sock.recv(3)
            type, command, success = struct.unpack('BBB', response_info)
            
            # Ignora a mensagem caso não seja uma resposta.
            if type != 2: continue
            
            # Informa sucesso ou fracasso da operação.
            if success == 1:
                print('Deu bom.')
            else:
                print('Deu ruim')       
            
        # DELETE: remove um arquivo do servidor.
        elif command == 'DELETE':
            try:
                # Envia a requisição.
                request = struct.pack(
                    f'BBB{len(args[0])}s',     # quatro inteiros
                    1,                          # código de requisição
                    2,                          # código do comando
                    len(args[0]),              # tamanho do nome do arquivo
                    bytes(args[0], 'utf-8'),   # nome do arquivo
                )
                sock.send(request)
                
                # Recebe a resposta do servidor.
                response_info = sock.recv(3)
                type, command, success = struct.unpack('BBB', response_info)

                # Ignora a mensagem caso não seja uma resposta.
                if type != 2: continue
            
                # Informa sucesso ou fracasso da operação.
                if success == 1:
                    print('Deu bom.')
                else:
                    print('Deu ruim')

            except Exception as e:
                print(f'Erro: {e}.')
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno

                print("Exception type: ", exception_type)
                print("File name: ", filename)
                print("Line number: ", line_number)
                continue


        elif command == 'GETFILESLIST':
            try:
                request = struct.pack(
                    'BBB',
                    1,              # código de requisição
                    3,              # código do comando
                    0               # não possui arquivo
                )
                sock.send(request)
                
                response_info = sock.recv(3)
                type, command, success = struct.unpack('BBB', response_info)

                if type != 2: continue
            
                if success == 1:
                    n_files, = struct.unpack('B', sock.recv(1))
                    print(f'Encontrados {n_files} arquivos.')

                    for _ in range(n_files):
                        filename_size, = struct.unpack('B', sock.recv(1))
                        filename = sock.recv(filename_size).decode('utf-8')
                        print(f'    {filename}')

                else:
                    print('Deu ruim')
                    continue

            except Exception as e:
                print(f'Erro: {e}')
                continue

        # GETFILE: Recebe um arquivo do servidor.
        elif command == 'GETFILE':
            try:
                request = struct.pack(
                    f'BBB{len(args[0])}s',
                    1,                          # código de requisição
                    4,                          # código do comando
                    len(args[0]),               # tamanho do nome do arquivo
                    bytes(args[0], 'utf-8'),   # nome do arquivo
                )
                sock.send(request)

                response_info = sock.recv(3)
                type, command, success = struct.unpack('BBB', response_info)
                
                if type != 2: continue
                
                if success == 1:
                    # Recebe o tamanho do arquivo
                    file_size, = struct.unpack('!I', sock.recv(4)) # ! = big-endian

                    # Cria o arquivo
                    file = open(f'{args[0]}', 'ab')

                    # Recebe cada byte e grava no arquivo
                    for _ in range(file_size):
                        file.write(bytes(sock.recv(1)))
                    
                    # Fecha o arquivo e marca operação como bem sucedida
                    file.close()
                    
                else:
                    print('Deu ruim')
                
            except Exception as e:
                print(f'Erro: {e}')
                continue

        elif command == 'EXIT': 
            sock.close()
            break

        elif command == '':
            continue

        else:
            print('Entrada inválida, tente novamente.')


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((ADDR, PORT))
    except:
        print('Conexão falhou, tente novamente.')
        return
    
    handle(sock)
    

if __name__ == '__main__':
    main()

    # Issues:
    # Cabeçalho
    # Comentários
    # Organizar (funções no handle)
    # getfilelist
    # revisar os comando
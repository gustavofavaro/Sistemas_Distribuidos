import socket
import hashlib

ADDR, PORT = '127.0.0.1', 55556

def handle(sock):
    while True:
        command, *args = input('Server> ').split(' ', 1)
        try:
            if not args: 
                sock.send(command.encode('utf-8'))
            else:
                sock.send(f'{command} {args[0]}'.encode('utf-8'))
            if command == 'EXIT':
                break
            response = sock.recv(1024).decode('utf-8')
            print(response)

        except Exception as e:
            print(f'Erro: {e}. Finalizando conexão.')
            sock.close()
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        command, *args = input('> ').split(' ', 1)
        
        if command == 'CONNECT':
            try:
                sock.connect((ADDR, PORT))
                user, passwd = args[0].split(', ')

                login = user + '#' + hashlib.sha512(str(passwd).encode('utf-8')).hexdigest()
                sock.send(login.encode('utf-8'))

                if sock.recv(1024).decode('utf-8') == 'SUCCESS':
                    print('Conectado!')
                    handle(sock)
                
                else:
                    print('Autenticação falhou, tente novamente.')
                    sock.close()

            except Exception as e:
                print(f'Erro: {e}')
        
        if command == 'EXIT':
            print('Saindo do programa.')
            return True

if __name__ == '__main__':
    main()
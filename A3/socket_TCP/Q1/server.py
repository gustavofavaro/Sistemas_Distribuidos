import threading
import socket
import os

# lista de usuários (o primeiro é um admin admin)
users = [('admin', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec')]

ADDR, PORT = '127.0.0.1', 55556

def send_message(conn, message):
    conn.send(message.encode('utf-8'))

def handle(conn, addr):
    help_file = open('help.txt')
    help_message = help_file.read()
    help_file.close()

    while True:
        message = conn.recv(1024).decode('utf-8')
        command, *arg = message.split(' ', 1)

        # Envia o diretório atual do servidor para o cliente
        if command == 'PWD':
            send_message(conn, os.getcwd())

        elif command == 'CHDIR':
            try:
                os.chdir(arg[0])
                send_message(conn, 'SUCCESS')
            except Exception as e:
                print(f'Erro no chdir: {e}')
                send_message(conn, 'ERROR')

        elif command == 'GETFILES':
            file_list = list(filter(os.path.isfile, os.listdir(path='.')))
            response = f'{len(file_list)}\n'
            for file_ in file_list:
                response += f'{file_}\n'
            send_message(conn, response)

        elif command == 'GETDIRS':
            dir_list = list(filter(os.path.isdir, os.listdir(path='.')))
            response = f'{len(dir_list)}\n'
            for dir in dir_list:
                response += f'{dir}\n'
            send_message(conn, response)

        elif command == 'EXIT':
            conn.close()
            break

        elif command == 'HELP':
            send_message(help_message)
        
        else:
            send_message('Comando inválido. Envie "HELP" para listar os comandos disponíveis.')
    
    print(f'Usuário com ip {addr[0]}:{addr[1]} saiu do servidor.')

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind((ADDR, PORT))
        sock.listen(10)
        while True:
            conn, addr = sock.accept()
            print(f'Usuário com ip {addr[0]}:{addr[1]} conectou-se ao servidor.')
            login = conn.recv(1024).decode('utf-8')
            user, passwd = login.split('#')
            if (user, passwd) in users:
                send_message(conn, 'SUCCESS')
                client_thread = threading.Thread(target=handle, args=(conn, addr))
                client_thread.start()
            else:
                send_message(conn, 'ERROR')
                conn.close()
                print(f'Usuário com ip {addr[0]}:{addr[1]} saiu do servidor.')

    except Exception as e:
        print(f'Erro: {e}')

if __name__ == '__main__':
    main()
import threading
import socket
import os

# lista de usuários (o primeiro é um admin admin)
users = [('admin', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec')]

ADDR, PORT = '127.0.0.1', 55555

def send_message(conn, message):
    conn.send(message).encode('utf-8')

def handle(conn):
    while True:
        message = conn.recv().decode('utf-8')
        command, *arg = message.split()

        # Envia o diretório atual do servidor para o cliente
        if command == 'PWD':
            send_message(os.getcwd())

        elif command == 'CHDIR':
            try:
                os.chdir(arg)
                send_message('SUCCESS')
            except Exception as e:
                print(f'Erro no chdir: {e}')
                send_message('ERROR')

        elif command == 'GETFILES':
            file_list = filter(os.isfile(), os.listdir(path='.'))
            response = f'{len(file_list)}\n'
            for file in file_list:
                response += f'{file}\n'
            send_message(response)

        elif command == 'GETDIRS':
            pass

        elif command == 'EXIT':
            conn.close()
            break
        
        else:
            send_message('UNKNOWN')

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind((ADDR, PORT))
        sock.listen(10)
        while True:
            conn, addr = sock.accept()
            print(f'Usuário com ip {addr[0]}:{addr[1]} conectou-se ao servidor.')
            login = conn.recv().decode('utf-8')
            if login in users:
                send_message(conn, 'SUCCESS')
                client_thread = threading.Thread(target=handle, args=(conn,))
                client_thread.start()
            else:
                send_message(conn, 'ERROR')
                conn.close()
                print(f'Usuário com ip {addr[0]}:{addr[1]} saiu do servidor.')

    except Exception as e:
        print(f'Erro: {e}')


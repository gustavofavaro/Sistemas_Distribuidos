#!/usr/bin/env python3
#-----------------------------------------------------------------------
# Autores: Fabricio Flávio Martins Damasceno e Gustavo Sengling Favaro
# Data de criação: 28/03/2023
# Data da última atualização: 10/04/2023
#-----------------------------------------------------------------------
""" Implementação do servidor da atividade de socket TCP Questão 1 utilizando socket TCP """
#-----------------------------------------------------------------------

import threading
import socket
import os

# lista de usuários (o primeiro é um admin admin).
users = [('admin', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec')]

# Endereço IP para o servidor.
ADDR, PORT = '127.0.0.1', 55555

# Envia uma mensagem no socket utilizando o método send().
def send_message(conn, message):
    conn.send(message.encode('utf-8'))

# Função que lida com as funções gerais do serivdor.
def handle(conn, addr):
    # Carrega um arquivo de texto contendo informações sobre os comandos.
    help_file = open('help/server_help.txt', 'r')            
    help_message = help_file.read()
    help_file.close()

    # Loop principal.
    while True:
        # Recebe a requisição do cliente e a separa em comando e argumentos.
        message = conn.recv(1024).decode('utf-8')
        command, *arg = message.split(' ', 1)

        # PWD: Envia o diretório atual do servidor para o cliente.
        if command == 'PWD':
            send_message(conn, os.getcwd())

        # CHDIR: Modifica o diretório atual do sistema de arquivos do Python (módulo 'os').
        # Envia o código SUCCESS para operação bem sucedida e ERROR para fallha.
        elif command == 'CHDIR':
            # Tratamendo de exceções para capturar um possível erro e responder ao cliente.
            try:
                os.chdir(arg[0])
                send_message(conn, 'SUCCESS')
            except Exception as e:
                print(f'Erro no chdir: {e}')
                send_message(conn, 'ERROR')

        # GETFILES: Envia a quantidade de arquivos e a lista dos mesmos no diretório atual do sistema de arquivos do Python.
        elif command == 'GETFILES':
            # Obtém a lista de arquivos.
            file_list = list(filter(os.path.isfile, os.listdir(path='.')))

            # Montagem da resposta a ser dada ao cliente incluindo o número de arquivos.
            response = f'Encontrados {len(file_list)} arquivos\n'

            # Adiciona o nome dos arquivos à resposta.
            for file_ in file_list:
                response += f'    {file_}\n'

            # Envio da resposta
            send_message(conn, response)

        # GETDIRS: Envia a quantidade de diretórios e a lista dos mesmos no diretório atual do sistema de arquivos do Python.
        elif command == 'GETDIRS':
            # Obtém a lista de diretórios.
            dir_list = list(filter(os.path.isdir, os.listdir(path='.')))

             # Montagem da resposta a ser dada ao cliente incluindo o número de diretórios.
            response = f'Encontrados {len(dir_list)} diretórios\n'
            
            # Adiciona o nome dos diretórios à resposta.
            for dir in dir_list:
                response += f'    {dir}\n'

            # Envio da resposta
            send_message(conn, response)

        # EXIT: Encerra a conexão com o cliente e interrompe o loop principal.
        elif command == 'EXIT':
            conn.close()
            break

        # HELP: Envia uma lista com os comandos disponíveis.
        elif command == 'HELP':
            send_message(conn, help_message)
        
        # Caso o comando não seja reconhecido, o servidor envia uma mensagem de falha, sugerindo o uso do comando HELP.
        else:
            send_message(conn, 'Comando inválido. Digite "HELP" para ver a lista de comandos do servidor.')
    
    # Quando o loop principal é quebrado, uma mensagem é emitida ao console do serivdor informando a saída do usuário.
    print(f'Usuário com ip {addr[0]}:{addr[1]} saiu do servidor.')

def main():
    # Criação do socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Servidor aberto.')
    
    try:
        # Método bind() para associar um endereço IP ao socket e listen() para preparar o mesmo para receber conexões.
        sock.bind((ADDR, PORT))
        sock.listen(10)

        # Loop principal
        while True:
            # Recebe uma conexão e emite uma mensagem ao console informando a conexão de um usuário.
            conn, addr = sock.accept()
            print(f'Usuário com ip {addr[0]}:{addr[1]} conectou-se ao servidor.')

            # Recebe a requisição de autenticação do cliente.
            login = conn.recv(1024).decode('utf-8')
            user, passwd = login.split('#')

            # Validação da tentativa de autenticação.
            if (user, passwd) in users:
                # Caso funcione, o servidor retorna a mensagem de sucesso e inicia uma thread para o cliente.
                send_message(conn, 'SUCCESS')
                client_thread = threading.Thread(target=handle, args=(conn, addr))
                client_thread.start()
            else:
                # Caso não funcione, o servidor retorna mensagem de erro e fecha a conexão com o cliente.
                send_message(conn, 'ERROR')
                conn.close()
                print(f'Usuário com ip {addr[0]}:{addr[1]} saiu do servidor.')

    except Exception as e:
        print(f'Erro: {e}')

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
#-----------------------------------------------------------------------
# Autores: Fabricio Flávio Martins Damasceno e Gustavo Sengling Favaro
# Data de criação: 28/03/2023
# Data da última atualização: 10/04/2023
#-----------------------------------------------------------------------
""" Implementação do cliente da atividade de socket TCP Questão 1 utilizando socket TCP """
#-----------------------------------------------------------------------

import socket
import hashlib

# Endereço IP para o servidor.
ADDR, PORT = '127.0.0.1', 55555

# Função que lida com o envio de requisições e recebimento de respostas do cliente.
def handle(sock):
    # Loop principal
    while True:
        # Recebe a entrada do usuário e a separa em comando e argumentos.
        command, *args = input('Server> ').split(' ', 1)
        try:
            # Ignora entrada vazia.
            if command == '':
                continue

            # Envia a requisição sem argumentos a mais além do comando.
            if not args: 
                sock.send(command.encode('utf-8'))

            # Envia a requisição com comando e argumentos.
            else:
                sock.send(f'{command} {args[0]}'.encode('utf-8'))

            # Interrompe o loop caso receba o comando de saída do servidor.
            if command == 'EXIT':
                print('Finalizando conexão com o servidor.')
                break

            # Recebe a resposta do servidor.
            response = sock.recv(1024).decode('utf-8')

            # Tratamento das possíveis respostas do servidor.
            if response == 'SUCCESS':
                print('Operação bem sucedida.')
            elif response == 'ERROR':
                print('Operação falhou. Tente novamente.')
            else:
                print(response)

        # Fecha a conexão caso haja algum erro.
        except Exception as e:
            print(f'Erro: {e}. Finalizando conexão.')
            sock.close()
            break


def main():
    # Criação do socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Loop principal
    while True:
        # Recebe as entradas do usuário e as separa em comando e argumentos.
        command, *args = input('> ').split(' ', 1)
        
        # CONNECT: Estabelece conexão com o servidor com a tentativa de autenticação.
        if command == 'CONNECT':
            try:
                # Verifica o formato da entrada para validar o comando.
                if ', ' not in args[0]:
                    raise Exception('Entrada inválida. Uso correto do commando CONNECT: "CONNECT <usuário>, <senha>"')
                
                # Separa os argumentos em usuário e senha e a codifica utilizando o algoritmo de criptografia SHA512.
                user, passwd = args[0].split(', ')
                login = user + '#' + hashlib.sha512(str(passwd).encode('utf-8')).hexdigest()

                # Realiza conexão com o servidor e envia os dados da autenticação.
                sock.connect((ADDR, PORT))
                sock.send(login.encode('utf-8'))

                # Recebe a resposta e verifica a resposta do servidor.
                if sock.recv(1024).decode('utf-8') == 'SUCCESS':
                    # Mensagem de sucesso e início da rotina de envio e recebimento de dados com o servidor.
                    print('Conexão estabelecida.')
                    handle(sock)
                
                else:
                    # Mensagem de erro e fecha a conexão com o servidor.
                    print('Autenticação falhou, tente novamente.')
                    sock.close()

            # Captura algum erro possível e o imprime na tela.
            except Exception as e:
                print(f'Erro: {e}')
        
        # EXIT: O programa principal é encerrado.
        elif command == 'EXIT':
            print('Saindo do programa.')
            return True
        
        # HELP: Envia uma lista com os comandos disponíveis.
        elif command == 'HELP':
            help_file = open('help/client_help.txt', 'r')
            print(help_file.read(), end='\n')
        
        # Ignora entrada vazia.
        elif command == '':
            continue

        # Inserção de comando inválido.
        else:
            print('Comando inválido. Digite HELP para ver a lista de comandos.')

if __name__ == '__main__':
    main()
Atividade TCP Questão 1
Autores: Fabricio Flávio Martins Damasceno e Gustavo Sengling Favaro
Data de criação: 28/03/2023

Como executar: abra dois terminais no diretório dos arquivos client.py e server.py e digite os seguintes comandos na dada ordem:
    1. Em um terminal, inicializar o servidor
    - Windows: py server.py
    - Linux: python3 server.py

    2. Em outro terminal, inicializar o cliente
    - Windows: py client.py
    - Linux: python3 client.py

Todas as funcionalidades disponíveis são operadas através do cliente.

Bibliotecas utilizadas:
- Threading: inicializar threads para realizar operações que ocorrem simultaneamente com conexões diferentes
- Socket: estabelecer uma conexão entre servidor e cliente utilizando Socket
- Os: realizar operações em um sistema operacional
- Hashlib: utilização de um algoritmo de criptografia

Exemplos de uso:
Servidor: apenas sua inicialização é necessária para que o mesmo funcione.
Cliente:
    - Conexão com o servidor e utilização de suas funções
    CONNECT admin, admin
    PWD
    CHDIR <diretório>
    GETFILES
    GETDIRS
    EXIT
    EXIT

    - Utilização dos comandos de ajuda para entender o funcionamento do programa
    HELP
    CONNECT admin, admin
    HELP
    EXIT
    EXIT
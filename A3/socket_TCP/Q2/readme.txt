Atividade TCP Questão 2
Autores: Fabricio Flávio Martins Damasceno e Gustavo Sengling Favaro
Data de criação: 03/04/2023

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
- Logging: realizar o registro das atividades realizadas no servidor
- Struct: conversão de dados para bytes para comunicação entre servidor e cliente

Exemplos de uso:
Servidor: apenas sua inicialização é necessária para que o mesmo funcione.
Cliente:
    - Operações de transferências de arquivos
    ADDFILE <arquivo_a_enviar>
    DELETE <arquivo_no_servidor>
    GETFILESLIST
    GETFILE <arquivo_no_servidor>
    EXIT
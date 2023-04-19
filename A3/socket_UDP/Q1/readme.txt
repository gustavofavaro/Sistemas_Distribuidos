Atividade UDP Questão 1
Autores: Fabricio Flávio Martins Damasceno e Gustavo Sengling Favaro
Data de criação: 04/04/2023

Como executar: abra dois terminais ou mais no diretório do arquivos client_p2p.py e digite os seguintes comandos na dada ordem:
    1. Em um terminal, inicializar o cliente
    - Windows: py client_p2p.py
    - Linux: python3 client_p2p.py

Bibliotecas utilizadas:
- Threading: inicializar threads para realizar operações que ocorrem simultaneamente com conexões diferentes
- Socket: estabelecer uma conexão entre os clientes utilizando Socket
- Struct: conversão de dados para bytes para comunicação
- Unicodedata: provê acesso ao banco de dados dos caracteres Unicode

Exemplos de uso:
Cliente Um:
    - Conexão com outro cliente e utilização das funcionalidades
    <Um nome de usuário>
    <Um endereço de IP seguido da porta> Ex: localhost:5555

Cliente Dois:
    <Um nome de usuário>
    <Um endereço de IP seguido da porta> Ex: localhost:7777
    CONNECT localhost:5555
    HELP
    <Qualquer mensagem> Ex: Teste
    <Link> Ex: https://www.google.com
    :<Nome de Emoji>: Ex: :GRINNING FACE:
    ECHO
    DISCONNECT localhost:7777
    EXIT

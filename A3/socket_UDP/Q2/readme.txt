Atividade UDP Questão 2
Autores: Fabricio Flávio Martins Damasceno e Gustavo Sengling Favaro
Data de criação: 18/04/2023

Como executar: abra dois terminais no diretório dos arquivos client.py e server.py e digite os seguintes comandos na dada ordem:
    1. Em um terminal, inicializar o servidor
    - Windows: py server.py
    - Linux: python3 server.py

    2. Em outro terminal, inicializar o cliente
    - Windows: py client.py
    - Linux: python3 client.py

Todas as funcionalidades disponíveis são operadas através do cliente.

import socket
import struct
import hashlib
import time
import threading
import psutil # pip install psutil (pega o espaço em disco do pc)
import platform # pega o SO do pc
import os

Bibliotecas utilizadas:
- Threading: inicializar threads para realizar operações que ocorrem simultaneamente com conexões diferentes
- Socket: estabelecer uma conexão entre servidor e cliente utilizando Socket
- Os: realizar operações em um sistema operacional
- Struct: conversão de dados para bytes para comunicação entre servidor e cliente
- Hashlib: utilização de um algoritmo de criptografia
- Time: pausar a execução do código por um momento
- Psutil: mesurar se o disco tem espaço o suficiente
- Platform: identificar o sistema operacional da máquina

Exemplos de uso:
Servidor: apenas sua inicialização é necessária para que o mesmo funcione.
Cliente:
    - Operações de transferências de arquivos
    UPLOAD <arquivo_a_enviar>
    SAIR
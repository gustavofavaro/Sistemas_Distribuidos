#!/usr/bin/env python3
#-----------------------------------------------------------------------
# Autores: Gustavo Sengling Favaro e Lucas Alexandre Seemund
# Data de criação: 09/07/2023
# Data da última atualização: 10/07/2023
#-----------------------------------------------------------------------
""" Implementação do coletor de mensagens utilizando uma base de dados e as enviando via RabbitMQ """
#-----------------------------------------------------------------------

import pandas as pd
import time
import pika

# Configurações do RabbitMQ
rabbitmq_host = 'localhost'

# Conectando-se ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Importando os tweets de um dataset
df = pd.read_csv('twitter_dataset.csv')

# Salvando cada tweet do dataset em uma lista
tweets = []
for index, row in df.iterrows():
    tweets.append(f'@{row["Username"]} says:\n"{row["Text"]}"')

count = 0
# Publicando postagens no RabbitMQ
for tweet in tweets:
    channel.basic_publish(exchange='', routing_key='twitter_queue', body=tweet)
    count += 1

    # Espera 1 segundo a cada 100 publicações enviadas
    if count % 50 == 0:
        print(f'{count} tweets sent.')
        time.sleep(1)

# Fechando a conexão
connection.close()
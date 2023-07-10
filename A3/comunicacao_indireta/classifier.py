#!/usr/bin/env python3
#-----------------------------------------------------------------------
# Autores: Gustavo Sengling Favaro e Lucas Alexandre Seemund
# Data de criação: 09/07/2023
# Data da última atualização: 10/07/2023
#-----------------------------------------------------------------------
""" Implementação do classificador de mensagens através de keywords e enviando-as via RabbitMQ """
#-----------------------------------------------------------------------

import pika

# Algumas keywords para filtrar três tópicos (política, futebol e séries de tv)
topics_keywords = {
    "politics": [
        "trump",
        "biden",
        "hillary",
        "elections",
        "government",
        "education",
        "corruption",
        "economy",
        "society",
        "legislation",
        "democracy",
        "human rights",
        "gun control"
    ],
    "tv_shows": [
        "game of thrones",
        "stranger things",
        "breaking bad",
        "friends",
        "the office",
        "the crown",
        "la casa de papel",
        "black mirror",
        "star wars",
        "ted lasso"
    ],
    "soccer": [
        "premier league",
        "la liga",
        "bundesliga",
        "serie A",
        "champions league",
        "world cup",
        "messi",
        "real madrid",
        "psg",
        "neymar",
        "cristiano ronaldo",
        "cr7",
        "haaland"
    ]
}

# Configurações do RabbitMQ
rabbitmq_host = 'localhost'

# Conectando-se ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Cria o canal para receber os tweets
channel.queue_declare(queue='twitter_queue')

# Cria canais para cada assunto específico
channel.queue_declare(queue='programming')
channel.queue_declare(queue='politics')
channel.queue_declare(queue='soccer')

# Função de retorno de chamada para processar as postagens do Twitter
def process_tweet(ch, method, properties, body):
    tweet = body.decode('utf-8')

    # Verificando palavras-chave para classificação
    for topic, keywords in topics_keywords.items():
        if any(keyword in tweet.lower() for keyword in keywords):
            channel.basic_publish(exchange='', routing_key=topic, body=tweet)
    

# Consumindo postagens do Twitter
channel.basic_consume(queue='twitter_queue', on_message_callback=process_tweet, auto_ack=True)

try:
    # Iniciando o consumo de mensagens
    print("Receiving messages...")
    channel.start_consuming()
    
except KeyboardInterrupt:
    # Capturando o KeyboardInterrupt (Ctrl+C) para sair do loop
    print("Keyboard Interrupt: stopping message receiving")
    channel.stop_consuming()

# Fechando a conexão
connection.close()
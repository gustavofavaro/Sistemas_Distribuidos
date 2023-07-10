import pika

topics_keywords = {
    "programming": ["python", "java", "C#", "machine learning", "frontend", "backend"],
    "football": ["premier league", "bundesliga", "la liga", "brasileirao", "libertadores", "champions league", "world cup"],
    "esports": ["league of legends", "csgo", "dota 2", "furia", "navi", "faze", "g2"]
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
channel.queue_declare(queue='football')
channel.queue_declare(queue='esports')

# Função de retorno de chamada para processar as postagens do Twitter
def process_tweet(ch, method, properties, body):
    tweet = body.decode('utf-8')

    # Verificando palavras-chave para classificação
    for topic, keywords in topics_keywords.items():
        if any(keyword in tweet for keyword in keywords):
            channel.basic_publish(exchange='', routing_key=topic, body=tweet.text)
    

# Consumindo postagens do Twitter
channel.basic_consume(queue='twitter_queue', on_message_callback=process_tweet, auto_ack=True)

try:
    # Iniciando o consumo de mensagens
    print("Recebendo mensagens do coletor.")
    channel.start_consuming()
    
except KeyboardInterrupt:
    # Capturando o KeyboardInterrupt (Ctrl+C) para sair do loop
    print("Interrupção de teclado. Encerrando o consumo de mensagens.")
    channel.stop_consuming()

# Fechando a conexão
connection.close()
import pika

# Imprime o tweet no console
def print_tweet(ch, method, properties, body):
    tweet = body.decode('utf-8')
    print(f'Assunto: {ch}\n{tweet}\n')

# Configurações do RabbitMQ
rabbitmq_host = 'localhost'

# Conectando-se ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Recebe a entrada do usuário
while True:
    try:
        # Recebe os tópicos por input
        wished_topics = input('Insira tópicos que você gostaria de receber tweets a respeito: ').split(', ')
        
        # Conecta aos tópicos recebidos
        for topic in wished_topics:
            channel.queue_declare(queue=topic)
            channel.basic_consume(queue=topic, on_message_callback=print_tweet, auto_ack=True)

        # Consumidor se conectou aos tópicos com sucesso, sai do loop de requisiçao
        break  

    except Exception as e:
        # Exibe os erros e repete o processo até que o usuário insira uma entrada válida
        print(str(e))

try:
    # Iniciando o consumo de mensagens
    print("Recebendo mensagens dos tópicos solicitados.")
    channel.start_consuming()

except KeyboardInterrupt:
    # Capturando o KeyboardInterrupt (Ctrl+C) para sair do loop
    print("Interrupção de teclado. Encerrando o consumo de mensagens.")
    channel.stop_consuming()

# Fechando a conexão
connection.close()
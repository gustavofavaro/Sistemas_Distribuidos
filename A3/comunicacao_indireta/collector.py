from dotenv import load_dotenv
import tweepy
import pika
import os
    
# Carrega variáveis de enviroment para carregar o tweepy
load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Realiza a autenticação e ativa a API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Configurações do RabbitMQ
rabbitmq_host = 'localhost'

# Conectando-se ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

def fetch_tweets(keywords):
    # Trata a entrada de keywords
    if isinstance(keywords, list):
        search_query = ' OR '.join(keywords)
    else:
        search_query = keywords
    
    # Faz a query de tweets baseada nas keywords recebidas
    tweets = api.search_tweets(q=search_query, count=5)

    # Retorna os tweets
    return tweets
    
# Publicando postagens no RabbitMQ
def publish_tweet(tweets):
    for tweet in tweets:
        channel.basic_publish(exchange='', routing_key='twitter_queue', body=tweet.text)

# Keywords de tópicos para adquirir tweets 
keywords_for_programming = ["python", "java", "C#", "machine learning", "frontend", "backend"],
keywords_for_football = ["premier league", "bundesliga", "la liga", "brasileirao", "libertadores", "champions league", "world cup"],
keywords_for_esports = ["league of legends", "csgo", "dota 2", "valorant", "loud", "furia", "navi", "faze", "g2"]

# Coleta tweets de programação e envia para a queue
tweets = fetch_tweets(keywords_for_programming)
publish_tweet(tweets)

# Coleta tweets de futebol e envia para a queue
tweets = fetch_tweets(keywords_for_football)
publish_tweet(tweets)

# Coleta tweets de esportes eletrônicos e envia para a queue
tweets = fetch_tweets(keywords_for_esports)
publish_tweet(tweets)

# Fecha o canal do RabbitMQ
connection.close()
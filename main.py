import os
import tweepy as twitter
import datetime as date

bearer_token = os.environ['TWITTER_TOKEN']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']


def concatenar_termos_candidato(entradas: list):
    return ' OR '.join(map(lambda termo: termo.replace(' ', '%20'), entradas))


def gerar_query(entradas: list):
    return '(' + concatenar_termos_candidato(entradas) + ') lang:pt -has:links -is:retweet'


formato_data = '%Y-%m-%dT%H:%M:01Z'
data_inicial = (date.datetime.now() - date.timedelta(hours=4)).strftime(formato_data)
data_final = date.datetime.now().strftime(formato_data)

client = twitter.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

candidatos = (['lula', 'Luiz Inacio Lula da Silva'], ['bolsonaro', 'Jair Messias Bolsonaro'], ['ciro', 'Ciro Gomes'],
              ['tebet', 'Simone Tebet'], ['doria', 'Joao Doria'], ['janones', 'Andre Janones'])
usuarios_buscados = {}
resultado_buscas = []

for entrada in candidatos:
    query = gerar_query(entrada)
    tweets_buscados = client.search_recent_tweets(query=query, max_results=100,
                                                  start_time=data_inicial, end_time=data_final,
                                                  tweet_fields=['author_id', 'created_at', 'public_metrics', 'source']).data
    resultado_buscas.extend(tweets_buscados)
    for tweet in tweets_buscados:
        if tweet.author_id not in usuarios_buscados:
            usuarios_buscados[tweet.author_id] = client.get_user(id=tweet.author_id,
                                                                 user_fields=['created_at', 'verified',
                                                                              'public_metrics', 'location']).data


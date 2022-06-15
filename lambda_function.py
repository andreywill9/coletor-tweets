import os
import time
import datetime as date
import pandas as pd
import json
import tweepy as twitter
import boto3

from io import StringIO  # python3; python2: BytesIO

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
data_inicial = (date.datetime.now() - date.timedelta(hours=1)).strftime(formato_data)
data_final = date.datetime.now().strftime(formato_data)

client = twitter.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

candidatos = (['lula', 'Luiz Inacio Lula da Silva'], ['bolsonaro', 'Jair Messias Bolsonaro'],
              ['ciro', 'Ciro Gomes'], ['tebet', 'Simone Tebet'], ['janones', 'Andre Janones'],
              ['marçal', 'Pablo Marçal'], ['bivar', 'Luciano Bivar'])

todos_tweets = []
usuarios_buscados = {}
resultado_buscas = []

print('Iniciando busca dos Tweets...')
for entrada in candidatos:
    print('Buscando Tweets sobre: ' + entrada[0] + '...')
    query = gerar_query(entrada)
    tweets_buscados = client.search_recent_tweets(query=query, max_results=30,
                                                  start_time=data_inicial, end_time=data_final,
                                                  tweet_fields=['author_id', 'created_at', 'public_metrics',
                                                                'source']).data

    if tweets_buscados is not None:
        todos_tweets.extend(tweets_buscados)
        print('Tweets buscados com sucesso!')
        print('Indo para próximo candidato...')
    else:
        print('candidato sem tweets relacionados no período de tempo buscado')
        print('Indo para próximo candidato...')
        pass
print('Tweets de todos os candidatos buscados com sucesso!')
print('Quantidade de Tweets buscados: ' + str(len(todos_tweets)))


print('Percorrendo cada um dos Tweets para buscar informações do autor...')
for tweet in todos_tweets:
    if tweet.author_id not in usuarios_buscados:
        usuarios_buscados[tweet.author_id] = client.get_user(id=tweet.author_id,
                                                             user_fields=['created_at', 'verified',
                                                                          'public_metrics', 'location'
                                                                          ]).data
    usuario = usuarios_buscados.get(tweet.author_id)
    linha = [0 for j in range(13)]
    linha[0] = tweet.id
    linha[1] = tweet.created_at.strftime(formato_data)
    linha[2] = tweet.text
    linha[3] = tweet.public_metrics.get('retweet_count')
    linha[4] = tweet.public_metrics.get('reply_count')
    linha[5] = tweet.public_metrics.get('like_count')
    linha[6] = tweet.source
    linha[7] = usuario.id
    linha[8] = usuario.username
    linha[9] = usuario.name
    linha[10] = usuario.created_at.strftime(formato_data)
    linha[11] = usuario.public_metrics.get('followers_count')
    linha[12] = usuario.verified
    resultado_buscas.append(linha)
print('Todos autores buscados!')

print('Gerando arquivo CSV...')
dataframe = pd.DataFrame(resultado_buscas)
dataframe.columns = ['id_tweet', 'data_tweet', 'texto', 'retweets', 'respostas', 'likes', 'fonte', 'id_usuario',
                     'arroba_usuario', 'nome_usuario', 'data_criacao_usuario', 'seguidores_usuario',
                     'usuario_verificado']

nome_data = str(date.datetime.now().strftime('%m%d_%H_%M_%S'))


def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client("s3")
    bucket = 'base-tweets-tgi'
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, index=False, sep=';', header=True)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, f'{nome_data}.csv').put(Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

import os
import tweepy as twitter

bearer_token = os.environ['TWITTER_TOKEN']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

data_inicial = '2022-05-08T21:39:01Z'
data_final = '2022-05-09T21:39:01Z'

client = twitter.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

candidatos = ['lula', 'bolsonaro']

for candidato in candidatos:
    query = candidato + " -has:links"
    tweets_buscados = client.search_recent_tweets(query=query, max_results=100,
                                                  start_time=data_inicial, end_time=data_final).data
    print("---------------------------------------------")
    for tweet in tweets_buscados:
        print(tweet.text)

import os
import tweepy as twitter
import datetime as date

bearer_token = os.environ['TWITTER_TOKEN']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

formato_data = '%Y-%m-%dT%H:%M:01Z'
data_inicial = (date.datetime.now() - date.timedelta(hours=4)).strftime(formato_data)
data_final = date.datetime.now().strftime(formato_data)

client = twitter.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

candidatos = ['lula', 'bolsonaro', 'ciro', 'doria']

for candidato in candidatos:
    query = candidato + " lang:pt -has:links"
    tweets_buscados = client.search_recent_tweets(query=query, max_results=100,
                                                  start_time=data_inicial, end_time=data_final).data
    print("\n---------------------------------------------\n")
    print("Quantidade tweets: " + str(len(tweets_buscados)))
    for tweet in tweets_buscados:
        print(tweet.text)

import pandas
import snscrape.modules.twitter as sntwitter

datas_coleta = [' since:2022-09-13 until:2022-09-14', ' since:2022-09-14 until:2022-09-15',
                ' since:2022-09-15 until:2022-09-16', ' since:2022-09-16 until:2022-09-17',
                ' since:2022-09-17 until:2022-09-18', ' since:2022-09-18 until:2022-09-19',
                ' since:2022-09-19 until:2022-09-20', ' since:2022-09-20 until:2022-09-21',
                ' since:2022-09-21 until:2022-09-22', ' since:2022-09-22 until:2022-09-23',
                ' since:2022-09-23 until:2022-09-24', ' since:2022-09-24 until:2022-09-25',
                ' since:2022-09-25 until:2022-09-26', ' since:2022-09-26 until:2022-09-27',
                ' since:2022-09-27 until:2022-09-28', ' since:2022-09-28 until:2022-09-29',
                ' since:2022-09-29 until:2022-09-30', ' since:2022-09-30 until:2022-09-01',
                ' since:2022-10-01 until:2022-10-02', ' since:2022-10-02 until:2022-10-03']
candidatos = ['lula', 'bolsonaro', 'ciro', 'simone tebet', 'eymael', 'sofia manzano', 'soraya', 'felipe d avila',
              'vera lucia', 'leo pericles']

lista_tweets = []
quantidade_maxima = 376
for data in datas_coleta:
    print(f'Coletando tweets de: {data}')
    for candidato in candidatos:
        contador = 0
        for tweet in sntwitter.TwitterSearchScraper(f'{candidato}{data}').get_items():
            if contador >= quantidade_maxima:
                break
            lista_tweets.append([tweet.id, tweet.date, tweet.content, '', '', '', '', '', '', '', '', '', ''])
            contador += 1
print('Todas as datas coletadas com sucesso')

dataframe = pandas.DataFrame(lista_tweets, columns=['id_tweet',
                                                    'data_tweet',
                                                    'texto',
                                                    'retweets',
                                                    'respostas',
                                                    'likes',
                                                    'fonte',
                                                    'id_usuario',
                                                    'arroba_usuario',
                                                    'nome_usuario',
                                                    'data_criacao_usuario',
                                                    'seguidores_usuario',
                                                    'usuario_verificado'])

dataframe.to_csv('bases/plano-b.csv')

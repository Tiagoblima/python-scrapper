
from datetime import datetime
from datetime import timedelta
from dateutil import parser
from tqdm import tqdm
from pygooglenews import GoogleNews
from newsfetch.news import newspaper
from multiprocessing import Pool
import pandas as pd
def entry_fun(entry):
  article = newspaper(entry['link'])
  if article:
    entry.update({"text":article.article})
    return entry
delta = timedelta(days=30)
gn = GoogleNews(lang = 'pt', country = 'BR')

topicos = ['mundo', 'Brasil', 'negócios', 'tecnologia', 'entreterimento', 'ciência', 'saúde']

news = []
for topic in tqdm(topicos):
  date = parser.parse("Jan 1 2010 12:00AM")
  for i in tqdm(range(96)):
    response = gn.search(topic,
                      from_=date.strftime('%Y-%m-%d'), 
                      to_=(date+delta).strftime('%Y-%m-%d'))
    with Pool(3) as p:
      articles = list(p.map(entry_fun,response['entries']))
    date += delta
    news.extend(articles)
news_df = pd.DataFrame(news)

news_df['published'] = pd.to_datetime(news_df['published'])
news_df.sort_values(by='published').to_csv('GoogleNews.csv')

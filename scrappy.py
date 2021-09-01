import pandas as pd
from tqdm import tqdm
import math
import time
import random 
from atpbar import flush

import time, random
from atpbar import atpbar
from newsfetch.news import newspaper
from multiprocessing import Pool
import numpy as np
news_df = pd.read_csv('GoogleNews.csv')

news_df = news_df.replace('https://www.youtube.com/.*', np.nan,regex=True).dropna()

print("size: ", news_df.shape[0])

news_df = news_df.iloc[:1000]

NUM_THREADS = 10 
indexes = range(0, news_df.shape[0], math.ceil(news_df.shape[0]/NUM_THREADS))
print(list(indexes))
#(indexes[slice(start=0,stop=df.shape[0], step=])
links_list = news_df['link'].tolist()

folds = [links_list[indexes[i]:indexes[i]+math.ceil(news_df.shape[0]/NUM_THREADS)] for i in range(len(indexes))]


import threading
def entry_fun(link):
  article = newspaper(link)

  entry = {"link": link}
  if article:
    entry.update({"text":article.article})
  return entry

articles = []
import multiprocessing
from atpbar import atpbar, register_reporter, find_reporter, flush
import more_itertools

multiprocessing.set_start_method('fork', force=True)

def f(xs):

    count = 0

    for x in atpbar(list(xs), name = multiprocessing.current_process().name):
        count += 1

    return count

items = range(80000000)
workloads = more_itertools.divide(8, items)

reporter = find_reporter()

with multiprocessing.Pool(8, register_reporter, [reporter]) as p:
    ret = p.map(f, workloads)
    flush()
    print(sum(ret))



pd.DataFrame(articles).to_csv('articlesNews.csv')
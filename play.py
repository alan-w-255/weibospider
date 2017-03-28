#%%
import codecs, sys
import json
import jieba
f = codecs.open('crawl.json', 'r', 'utf-8','ignore')
data = json.load(f)
data
for x in data:
    try:
        t = jieba.cut(x['mblog_text'])
        for y in t:
            print(y)
    except KeyError:
        pass
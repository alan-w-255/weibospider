#%%
import codecs, sys
import json
import jieba
import re
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def stop(s, sw):
    for x in sw:
        s = s.replace(x, '')
    return s

stop_words=(
    '转发微博',
    '//',
    '😓',
    '👍',
    '【',
    '】',
    '#',
    '😂',
    '＃',
)

jieba.add_word('转发微博')



f = codecs.open('out.json', 'r', 'utf-8','replace')
data = json.load(f)
for x in data:
    try:
        y = strip_tags(x['mblog_text'])
        y = stop(y, stop_words)
        t = jieba.cut(y)
        print("cut: ", end=' ')
        print(', '.join(t))
    except KeyError:
        pass





    
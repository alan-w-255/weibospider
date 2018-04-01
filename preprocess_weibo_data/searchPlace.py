import requests
from bs4 import BeautifulSoup



def getWikiTags(placeName):
    """
    输入地名, 返回从百度百科上爬取地名的标签
    """
    tpl_url = "https://baike.baidu.com/item/{keywd}"
    s = requests.session()
    s.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    res = s.get(tpl_url.format(keywd=placeName))
    soup = BeautifulSoup(res.text, 'lxml')
    open_tag_item = soup.find('dd', id='open-tag-item')
    results = []
    if open_tag_item is not None:
        tags = open_tag_item.find_all('span', class_='taglist')
        for t in tags:
            results.append(t.text.encode(res.encoding).decode('utf8')
            .strip('\n').strip(',').strip('，').strip())
    return results



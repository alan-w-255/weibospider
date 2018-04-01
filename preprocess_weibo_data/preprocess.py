# encoding: utf-8
import pymongo
import json
from searchPlace import getWikiTags

client = pymongo.MongoClient()
db = client['wbdata']
collection = db['scrapy_items']
processed_collection = db['preprocessed_items']

placeArray=["色达","达州","成都","稻城","稻城亚丁","青城山","泸定","黄龙","九寨沟","海螺沟","都江堰","金沙","泸沽湖","乐山","峨眉","自贡","攀西","川藏","泸州","杜甫草堂","蒲江","彭州","贡嘎","宽窄巷子","锦里","阆中","蜀南","合江亭","春熙路","西岭","四姑娘山","九眼桥","攀枝花","犀浦","川外","金顶","千佛顶","亚青寺","新都桥","西岭雪山","武侯祠","红原","大渡河","金川","达古冰川","平乐古镇","凉山","毕棚沟","阿坝","文殊院","祠堂街","鹧鸪山自然公园","横江古镇","郫都","丹巴","西昌","诺尔盖","黄龙溪","红岩顶","牛背山","喇叭河","雅安","上里古镇","望鱼古镇","达瓦更扎","桃平羌寨","康定","木格措","巴朗山","法藏寺""燕子沟","南充","青居镇","甘孜","塔公草原","安仁古镇","牟尼沟","冬玛嘉沟","白岩寺","松坪沟","龙苍沟","什邡","冶勒水库","月亮湖","孟获城草甸","人民公园","绵阳","寻龙山","二郎山","东拉山"]

placeTagDict = {}
for p in placeArray:
    tags = getWikiTags(p)
    placeTagDict[p] = tags
    print(p, tags)


f = open("./out4.json", "a", encoding="utf8")
f.write("[\n")
for doc in collection.find():
    weibo_text_places_and_tags = []
    for p in placeArray:
        if p in doc['mblog_text']:
            placeAndTags = ({"place": p, "tags": placeTagDict[p]})
            print(placeAndTags)
            weibo_text_places_and_tags.append(placeAndTags)
    doc = {"scheme":doc["scheme"] ,"weibo_places": weibo_text_places_and_tags, "created_at": doc["created_at"]}
    f.write(json.dumps(doc, ensure_ascii=False))
    processed_collection.insert(doc)
f.write("\n]")
f.close()

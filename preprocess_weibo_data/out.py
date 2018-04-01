import pymongo
import json
client = pymongo.MongoClient()
db = client['wbdata']
collection = db['preprocessed_items']

with open("./out4.txt", "w", encoding="utf-8") as f:
    for doc in collection.find({}, {"_id": False}):
        json.dump(doc, f, ensure_ascii=False)
        f.write("\n")

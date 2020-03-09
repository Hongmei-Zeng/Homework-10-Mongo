import requests
import pymongo

BASE_URL = "https://am4.syn-api.com/api/6/asset/list/client/showcase/vendor/WatchMojo/genres/Sports/media_scheme/mp4/expand/list/rows/25/language/en"
CONN = "mongodb://localhost:27017"
client = pymongo.MongoClient(CONN)
db = client.nhl_db

resp = requests.get(BASE_URL)
results = resp.json()["results"]

for result in results:
    db.news.insert_one(result)

results_from_db = [result for result in db.news.find()]
print(results)
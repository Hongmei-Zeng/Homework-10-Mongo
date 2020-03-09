import pymongo
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.DATABASENAME  # db = client.fruits_db
fruits = db.fruits_db     # create a collection "fruits"
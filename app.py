from scrape_mars import scrape
import pymongo
from flask import Flask, render_template

app = Flask(__name__)

CONN = "mongodb://localhost:27017"

client = pymongo.MongoClient(CONN)
db = client.mars_db
db.mars.drop()
db.mars.insert_one(scrape())

@app.route("/")
def index():
    results = list(db.mars.find())
    return render_template("index.html", items=results)

@app.route("/scrape")
def scrapedata():
    return scrape()

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask
import pymongo

app = Flask(__name__)

# uri = "mongodb://mongo:27017" # uri docker
uri = "mongodb://localhost:27017"

mongo_client = pymongo.MongoClient(uri)
db = mongo_client["vroomlegend"]


@app.route('/')
def test1():
    collection = db["user"]
    data = {"email": "test@gmail.com", "mdp": "wow"}
    collection.insert_one(data)
    return "pass"


@app.route('/find')
def test2():
    collection = db["user"]
    for doc in collection.find({"email": "test@gmail.com"}):
        print(doc)
    return "pass"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

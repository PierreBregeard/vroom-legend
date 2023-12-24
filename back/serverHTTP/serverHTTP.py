from flask import Flask, request
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# uri = "mongodb://mongo:27017" # uri docker
uri = "mongodb://localhost:27017"

mongo_client = pymongo.MongoClient(uri)
db = mongo_client["vroomlegend"]


@app.route('/')
def test1():
    collection = db["user"]
    data = {"email": "mich@gmail.com", "mdp": generate_password_hash('test'),
            "car": {"color1": "bleu", "color2": "vert"},
            "history": [{"id_map": 1, "rank": 2, "time": "11:20:10"}, {"id_map": 2, "rank": 3, "time": "12:50:40"}]}
    collection.insert_one(data)
    return "pass"


@app.route('/find')
def test2():
    collection = db["user"]
    for doc in collection.find({"email": "test@gmail.com"}):
        print(doc)
    return "pass"

@app.route('/inscription', methods=['POST'])
def inscription():
    collection = db["user"]
    data = request.json
    data['mdp'] = generate_password_hash(data['mdp'])
    collection.insert_one(data)
    print(data)
    return "oui"

@app.route('/connexion', methods=['POST'])
def connexion():
    collection = db["user"]
    data = request.json
    user = collection.find_one({"email": data["email"]})
    print(user)
    if user and check_password_hash(user['mdp'], data['mdp']):
        print(data)
        return 'il est dedans'
    else:
        return 'pas dedans'

@app.route('/couleur')
def couleur():
    collection = db["user"]
    data = request.json
    color = collection.find_one({"email": data["email"]}, {"car"})
    print(color)
    return 'couleur'

@app.route('/changeCoul', methods=['POST'])
def changeCouleur():
    collection = db["user"]
    data = request.json
    color = collection.find_one({"email": data["email"]}, {"car"})
    if color.get("car") is None:
        coul = collection.update_one({"email": data["email"]}, {"$set": {"car": data["car"]}})
    else :
        coul = collection.update_one({"email": data["email"]}, {"$set": {"car": data["car"]}})
    return 'ça a changé la coul'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

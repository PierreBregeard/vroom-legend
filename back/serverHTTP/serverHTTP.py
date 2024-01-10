from flask import Flask, request, session, jsonify
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# uri = "mongodb://mongo:27017" # uri docker
uri = "mongodb://localhost:27017"

mongo_client = pymongo.MongoClient(uri)
db = mongo_client["vroomlegend"]


@app.route('/inscription', methods=['POST'])
def inscription():
    collection = db["user"]
    data = request.json
    data['mdp'] = generate_password_hash(data['mdp'])
    user = collection.find_one({"pseudo": data["pseudo"]})
    useremail = collection.find_one({"email": data["email"]})
    if user is None and useremail is None:
        collection.insert_one(data)
        print(data)
        return "oui"
    else:
        return "mon reuf ????"

@app.route('/saveHistory', methods=['POST'])
def saveHistory():
    collection = db["user"]
    data = request.json
    user = collection.find_one({"pseudo": data["pseudo"]})
    collection.update_one({"pseudo": data["pseudo"]}, {"$push": {"parties": data["parties"]}})
    return "je t'ai save ca mg"

@app.route('/connexion', methods=['POST'])
def connexion():
    collection = db["user"]
    data = request.json
    user = collection.find_one({"email": data["email"]})
    print(user)
    if user and check_password_hash(user['mdp'], data['mdp']):
        print(data)
        return str(user['pseudo'])
    else:
        return 'pas dedans'


@app.route('/couleur')
def couleur():
    collection = db["user"]
    data = request.json
    color = collection.find_one({"pseudo": data["pseudo"]}, {"car"})
    print(color)
    return 'couleur'

@app.route('/changeCoul', methods=['POST'])
def changeCouleur():
    collection = db["user"]
    data = request.json
    color = collection.find_one({"pseudo": data["pseudo"]}, {"car"})
    if color.get("car") is None:
        coul = collection.update_one({"pseudo": data["pseudo"]}, {"$set": {"car": data["car"]}})
    else :
        coul = collection.update_one({"pseudo": data["pseudo"]}, {"$set": {"car": data["car"]}})
    return 'ça a changé la coul'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

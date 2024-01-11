from flask import Flask, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# uri = "mongodb://mongo:27017" # uri docker
uri = "mongodb+srv://michelrecchia1:VroomLegends@animes.kflm1cp.mongodb.net/?retryWrites=true&w=majority"

mongo_client = MongoClient(uri, server_api=ServerApi('1'))
db = mongo_client["VroomLegends"]


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
        return ""
    else:
        return ""


@app.route('/saveHistory', methods=['POST'])
def saveHistory():
    collection = db["user"]
    data = request.json
    user = collection.find_one({"pseudo": data["pseudo"]})
    collection.update_one({"pseudo": data["pseudo"]}, {"$push": {"parties": data["parties"]}})
    return ""


@app.route('/getHistory', methods=['POST'])
def getHistory():
    collection = db["user"]
    data = request.json
    user = collection.find_one({"pseudo": data["pseudo"]})
    return user['parties']

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
        return ''


@app.route('/couleur', methods=["POST"])
def couleur():
    collection = db["user"]
    data = request.json
    print(data["pseudo"])
    color = collection.find_one({"pseudo": data["pseudo"]}, {"car"})
    if color.get("car") is not None:
        return str(color["car"])
    else:
        return ""


@app.route('/changeCoul', methods=['POST'])
def changeCouleur():
    collection = db["user"]
    data = request.json
    color = collection.find_one({"pseudo": data["pseudo"]}, {"car"})
    coul = collection.update_one({"pseudo": data["pseudo"]}, {"$set": {"car": data["car"]}})
    return ''


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

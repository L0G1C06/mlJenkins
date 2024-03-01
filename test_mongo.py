import pymongo
import hashlib

client = pymongo.MongoClient("mongodb+srv://root:root@mlartifact.ihopp5t.mongodb.net/?retryWrites=true&w=majority&appName=MLArtifact")

db = client["MLArtifact"]
collection = db["MLArtifact"]

hash = hashlib.sha256(b"Teste de Hash").hexdigest()

artifact = {"Hash": hash, "artifact": {"weight": 0.78, "developer": "Eduardo"}}

collection.insert_one(artifact)

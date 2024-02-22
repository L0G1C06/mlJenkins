from tinydb import TinyDB, Query

db = TinyDB('data_hashes.json')

def insert_hash(name, hash_value, data_type):
    db.upsert({'name': name, data_type: hash_value}, Query().name == name)

def retrieve_hash(name, data_type):
    result = db.search(Query().name == name)
    return result[0][data_type] if result else None
import sqlite3 
from hashlib import sha256
import json
from tinydb import TinyDB, Query

db = TinyDB('data_hashes.json')
conn_data = sqlite3.connect("./versioning/data.db")
conn_model = sqlite3.connect("./versioning/model.db")
cur_data = conn_data.cursor()
cur_model = conn_model.cursor()

def create_data_versioning():
    cur_data.execute("""CREATE TABLE IF NOT EXISTS data_versioning (
                id TEXT,
                data TEXT,
                metadata TEXT
    )""")

def generate_hash(text):
    return sha256(text.encode('utf-8')).hexdigest()

def check_data_hash(hash_id):
    cur_data.execute("SELECT 1 FROM data_versioning WHERE id = ?", (hash_id,))
    result = cur_data.fetchone()
    return result is not None 

def retrieve_hash(name, data_type):
    result = db.search(Query().name == name)
    return result[0][data_type] if result else None

def insert_model_versioning(hash_id, image, metadata):
    metadata_json = json.dumps(metadata)
    cur_model.execute("INSERT INTO model_versioning VALUES (?, ?, ?)", (hash_id, image, metadata_json))
    conn_model.commit()
    #conn_model.close()

def insert_data_versioning(hash_id, dataset_used, metadata):
    metadata_json = json.dumps(metadata)
    cur_data.execute("INSERT INTO data_versioning VALUES (?, ?, ?)", (hash_id, dataset_used, metadata_json))
    conn_data.commit()
    #conn_data.close()

def get_data_table():
    with conn_data:
        cur_data.execute("SELECT * FROM data_versioning")
        return cur_data.fetchall()
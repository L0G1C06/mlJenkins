import sqlite3 
from hashlib import sha256

conn_data = sqlite3.connect("data.db")
conn_model = sqlite3.connect("model.db")
cur_data = conn_data.cursor()
cur_model = conn_model.cursor()

def create_data_versioning():
    cur_data.execute("""CREATE TABLE IF NOT EXISTS data_versioning (
                id TEXT PRIMARY KEY,
                data TEXT,
                metadata TEXT
    )""")

def generate_hash(text):
    return sha256(text.encode('utf-8')).hexdigest()

def insert_model_versioning(model_hash, image, metadata):
    cur_model.execute("INSERT INTO model_versioning VALUES (?, ?, ?)", (model_hash, image, metadata))
    conn_model.commit()
    conn_model.close()

def insert_data_versioning(data_hash, dataset_used, metadata):
    cur_data.execute("INSERT INTO data_versioning VALUES (?, ?, ?)", (data_hash, dataset_used, metadata))
    conn_data.commit()
    conn_data.close()

if __name__ == "__main__":
    insert_data_versioning(generate_hash("Hello"), "DatasetV1", "MetadataV1")
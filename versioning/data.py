import os 
import shutil 
import json 
import hashlib 
from datetime import datetime 

from .database import retrieve_hash, insert_hash

def calculate_dir_hash(dir_path):
    hash_object = hashlib.sha256()
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as f:
                while chunk := f.read(4096):
                    hash_object.update(chunk)
                hash_object.update(str(os.path.getmtime(file_path)).encode())  # Include modification time in hash
    return hash_object.hexdigest()

def create_dataset_version(metadata, data_dir='./data/'):
    # Calculate hash of the model file
    data_hash = calculate_dir_hash(data_dir)
    
    # Check if data hash already exists in the database
    existing_data_hash = retrieve_hash('data_version_hash', 'data_hash')
    if existing_data_hash == data_hash:
        return existing_data_hash
    
    # Save data hash to the database
    insert_hash('data_version_hash', data_hash, 'data_hash')
    
    # Create version directory if it doesn't exist
    version_dir = os.path.join('data_versioning', data_hash)
    os.makedirs(version_dir, exist_ok=True)

    # Copy model files to version directory
    shutil.copytree(data_dir, os.path.join(version_dir, 'data'))

    # Add creation date and hyperparameters to metadata
    metadata['creation_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save metadata to a JSON file
    with open(os.path.join(version_dir, 'metadata.json'), 'w') as metadata_file:
        json.dump(metadata, metadata_file)

    return data_hash

def get_data_version(version_hash):
    version_dir = os.path.join('data_versioning', version_hash)
    if os.path.exists(version_dir):
        return version_dir 
    else:
        return None
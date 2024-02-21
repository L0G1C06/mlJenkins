import os 
import shutil 
import json 
import hashlib 
from datetime import datetime

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

def create_dataset_version(metadata, data_dir = './data/'):
    # Calculate hash of the model file
    model_hash = calculate_dir_hash(data_dir)
    
    version_dir = os.path.join('data_versioning', model_hash)
    os.makedirs(version_dir, exist_ok=True)

    # Copy model files to version directory
    shutil.copytree(data_dir, os.path.join(version_dir, 'data'))

    # Add creation date and hyperparameters to metadata
    metadata['creation_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save metadata to a JSON file
    with open(os.path.join(version_dir, 'metadata.json'), 'w') as metadata_file:
        json.dump(metadata, metadata_file)

    return model_hash

def get_data_version(version_hash):
    version_dir = os.path.join('data_versioning', version_hash)
    if os.path.exists(version_dir):
        return version_dir 
    else:
        return None
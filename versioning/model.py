import os 
import shutil 
import json 
import hashlib 
from datetime import datetime 


def calculate_directory_hash(directory_path):
    hash_object = hashlib.sha256()
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as f:
                while chunk := f.read(4096):
                    hash_object.update(chunk)
                hash_object.update(str(os.path.getmtime(file_path)).encode())  # Include modification time in hash
    return hash_object.hexdigest()

def create_model_version(metadata, model_dir = './my-model/', data_used = None, creator = None, epochs = None, learning_rate = None, optimizer = None):
    # Calculate hash of the model file
    model_hash = calculate_directory_hash(model_dir)
    
    version_dir = os.path.join('model_versioning', model_hash)
    os.makedirs(version_dir, exist_ok=True)

    # Copy model files to version directory
    shutil.copytree(model_dir, os.path.join(version_dir, 'model'))

    # Add creation date and hyperparameters to metadata
    metadata['creation_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata['creator'] = creator
    metadata['dataset_used'] = data_used
    metadata['hyperparameters'] = {'epochs': epochs, 'learning_rate': learning_rate, 'optimizer': optimizer}

    # Save metadata to a JSON file
    with open(os.path.join(version_dir, 'metadata.json'), 'w') as metadata_file:
        json.dump(metadata, metadata_file)

    return model_hash

def get_model_version(version_hash):
    version_dir = os.path.join('model_versioning', version_hash)
    if os.path.exists(version_dir):
        return version_dir
    else:
        return None
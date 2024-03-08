import os 
import shutil 
import json 
import hashlib 
import subprocess
from datetime import datetime 

from .database import insert_model_versioning

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

def get_installed_libraries():
    # Use pip to list installed packages and versions
    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, text=True)
    installed_packages = result.stdout.strip().split('\n')
    libraries = {}
    for package in installed_packages:
        name, version = package.split('==')
        libraries[name] = version
    return libraries

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
    metadata['environment'] = get_installed_libraries()

    # Save metadata to a JSON file
    with open(os.path.join(version_dir, 'metadata.json'), 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=2, separators=(',', ': '))

    insert_model_versioning(model_hash, "Image: TO DO", metadata)

    return model_hash

def get_model_version(version_hash):
    version_dir = os.path.join('model_versioning', version_hash)
    if os.path.exists(version_dir):
        return version_dir
    else:
        return None
    
def save_hash_on_file(hash_to_insert):
    existing_hashes = []
    if os.path.exists("model_hashes.txt"):
        with open("model_hashes.txt", "r") as f:
            existing_hashes = f.readlines()

    existing_hashes.insert(0, hash_to_insert + "\n")
    with open("model_hashes.txt", "w") as f:
        f.writelines(existing_hashes)
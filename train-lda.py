import os
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pandas as pd
from joblib import dump
from sklearn import preprocessing
import argparse

from versioning import model, data, database

# Load directory paths for persisting model

MODEL_DIR = "./my-model/"
MODEL_FILE_LDA = "clf_lda.joblib"
MODEL_PATH_LDA = os.path.join(MODEL_DIR, MODEL_FILE_LDA)

def train():

    # Load, read and normalize training data
    training = "./data/train.csv"
    data_train = pd.read_csv(training)

    y_train = data_train['# Letter'].values
    X_train = data_train.drop(data_train.loc[:, 'Line':'# Letter'].columns, axis = 1)
    
    # Data normalization (0,1)
    X_train = preprocessing.normalize(X_train, norm='l2')

    # Models training

    # Linear Discrimant Analysis (Default parameters)
    clf_lda = LinearDiscriminantAnalysis()
    clf_lda.fit(X_train, y_train)

    # Serialize model
    dump(clf_lda, MODEL_PATH_LDA)

    print(f"Model trained and saved on {MODEL_PATH_LDA}")

if __name__ == '__main__':
    train()
    parser = argparse.ArgumentParser(description='Create a new version of the model with specified hyperparameters.')
    parser.add_argument('--model_dir', type=str, default=MODEL_DIR, help='Path to the model directory')
    parser.add_argument('--creator', type=str, default='', help='Name of model developer')
    parser.add_argument('--data_used', type=str, default='./data/')
    parser.add_argument('--epochs', type=int, default=0, help='Number of epochs')
    parser.add_argument('--learning_rate', type=float, default=0.0, help='Learning rate')
    parser.add_argument('--optimizer', type=str, default='', help='Optimizer used for training')
    args = parser.parse_args()
    metadata = {}
    data_version_hash = data.create_dataset_version(metadata, data_dir=args.data_used)
    previous_data_version_hash = database.retrieve_hash('data_version_hash', 'data_hash')
    if data_version_hash is None:
        print("Failed to generate data hash")
        exit()
    if data_version_hash == previous_data_version_hash:
        model_version_hash = model.create_model_version(metadata, model_dir=args.model_dir, data_used=previous_data_version_hash, creator=args.creator, epochs=args.epochs, learning_rate=args.learning_rate, optimizer=args.optimizer)
        save_hash = model.save_hash_on_file(model_version_hash)
    else:
        model_version_hash = model.create_model_version(metadata, model_dir=args.model_dir, data_used=data_version_hash, creator=args.creator, epochs=args.epochs, learning_rate=args.learning_rate, optimizer=args.optimizer)
        save_hash = model.save_hash_on_file(model_version_hash)
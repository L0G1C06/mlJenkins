import os
import numpy as np
from sklearn.neural_network import MLPClassifier
import pandas as pd
from joblib import dump, load
from sklearn import preprocessing

def train():

    # Load directory paths for persisting model

    MODEL_DIR = "./my-model/"
    MODEL_FILE_NN = "clf_nn.joblib"
    MODEL_PATH_NN = os.path.join(MODEL_DIR, MODEL_FILE_NN)

    # Load, read and normalize training data
    training = "./data/train.csv"
    data_train = pd.read_csv(training)

    y_train = data_train['# Letter'].values
    X_train = data_train.drop(data_train.loc[:, 'Line':'# Letter'].columns, axis = 1)

    # Data normalization (0,1)
    X_train = preprocessing.normalize(X_train, norm='l2')

    # Models training

    # Neural Networks multi-layer perceptron (MLP) algorithm
    clf_NN = MLPClassifier(solver='adam', activation='relu', alpha=0.0001, hidden_layer_sizes=(500,), random_state=0, max_iter=1000)
    clf_NN.fit(X_train, y_train)

    # Serialize model
    dump(clf_NN, MODEL_PATH_NN)

    # Load, read and normalize training data
    testing = "./data/test.csv"
    data_test = pd.read_csv(testing)

    y_test = data_test['# Letter'].values
    X_test = data_test.drop(data_test.loc[:, 'Line':'# Letter'].columns, axis = 1)

    # Data normalization (0,1)
    X_test = preprocessing.normalize(X_test, norm='l2')

    # Load and Run model
    clf_nn = load(MODEL_PATH_NN)
    
    print(int(clf_nn.score(X_test, y_test)*100))

if __name__ == '__main__':
    train()

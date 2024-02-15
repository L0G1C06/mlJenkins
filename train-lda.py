import os
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pandas as pd
from joblib import dump
from sklearn import preprocessing

def train():

    # Load directory paths for persisting model

    MODEL_DIR = "./my_model/"
    MODEL_FILE_LDA = "clf_lda.joblib"
    MODEL_PATH_LDA = os.path.join(MODEL_DIR, MODEL_FILE_LDA)

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
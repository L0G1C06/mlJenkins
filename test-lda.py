import pandas as pd 
from sklearn import preprocessing
from joblib import load 
import os 

def test():
    MODEL_DIR = "./my_model/"
    MODEL_FILE_LDA = "clf_lda.joblib"
    MODEL_PATH_LDA = os.path.join(MODEL_DIR, MODEL_FILE_LDA)

    testing = "test.csv"
    data_test = pd.read_csv(testing)
    y_test = data_test['# Letter'].values
    X_test = data_test.drop(data_test.loc[:, 'Line':'# Letter'].columns, axis = 1)
    # Data normalization (0,1)
    X_test = preprocessing.normalize(X_test, norm='l2')
    # load and Run model
    clf_lda = load(MODEL_PATH_LDA)

    score = int(clf_lda.score(X_test, y_test)*100)
    print(f"Precision: {score}%")

if __name__ == "__main__":
    test()
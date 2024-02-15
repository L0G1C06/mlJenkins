FROM python:3.8

RUN mkdir my-model
ENV MODEL_DIR=/my-model/
ENV MODEL_FILE_LDA=clf_lda.joblib
ENV MODEL_FILE_NN=clf_nn.joblib

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY /data/train.csv ./data/train.csv
COPY /data/test.csv ./data/test.csv

COPY train-lda.py ./train-lda.py
COPY train-nn.py ./train-nn.py
COPY train-auto-nn.py ./train-auto-nn.py
COPY test-lda.py ./test-lda.py

RUN python3 train-lda.py
RUN python3 test-lda.py
#RUN python3 train-nn.py

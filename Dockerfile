FROM python:3.8 

#RUN mkdir my-model 
#RUN mkdir versioning
#
#ENV MODEL_DIR=/my-model/
#ENV MODEL_FILE_LD=clf_lda.joblib
#ENV MODEL_FILE_NN=clf_nn.joblib 
#
#COPY requirements.txt ./requirements.txt 
#RUN pip install -r requirements.txt 
#
#COPY versioning/ ./versioning/
#
#COPY /data/train.csv ./data/train.csv 
#COPY /data/test.csv ./data/test.csv
#
#COPY train-lda.py ./train-lda.py
#COPY train-nn.py ./train-nn.py
#COPY train-auto-nn.py ./train-auto-nn.py
#COPY test-lda.py ./test-lda.py
#
#RUN python3 train-lda.py
#RUN python3 test-lda.py
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY . /code/

EXPOSE 8001

CMD ["python3", "main.py"]
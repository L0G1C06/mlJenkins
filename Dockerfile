FROM python:3.8 

WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt 

RUN pip install -r /code/requirements.txt 

COPY . /code/app 

CMD ["python3", "app/main.py"]
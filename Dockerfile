# Dockerfile, Image, Container
FROM python:3.9-slim-buster

WORKDIR /crop-gen

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENV FLASK_APP=main.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
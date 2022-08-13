FROM python:3.8-slim

WORKDIR /usr/app

RUN apt-get update
RUN apt-get install ffmpeg -y


COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT python ./server.py
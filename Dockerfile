FROM python:3.7

RUN apt-get update -y

RUN useradd -m server

COPY ./requirements.txt /home/server/requirements.txt

RUN pip install -r /home/server/requirements.txt

COPY ./config.yml /home/server/config.yml

RUN chown -R server:server /home/server

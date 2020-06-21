FROM python:3.7

RUN apt-get update -y

RUN useradd -m server

COPY ./requirements.txt /home/server/requirements.txt
RUN pip install -r /home/server/requirements.txt

COPY ./config.docker.yml /home/server/config.yml
COPY ./start.sh /home/server/start.sh
COPY ./erica /home/server/erica
COPY ./commands /home/server/commands

RUN chown -R server:server /home/server

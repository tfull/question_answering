FROM python:3.7

RUN apt-get update -y

RUN useradd -m server

RUN apt-get install build-essential cmake -y
RUN wget https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc3/jumanpp-2.0.0-rc3.tar.xz -P /tmp
WORKDIR /tmp
RUN tar xvf jumanpp-2.0.0-rc3.tar.xz
WORKDIR /tmp/jumanpp-2.0.0-rc3
RUN mkdir build
WORKDIR /tmp/jumanpp-2.0.0-rc3/build
RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local
RUN make
RUN make install

WORKDIR /

COPY ./requirements.txt /home/server/requirements.txt
RUN pip install -r /home/server/requirements.txt

COPY ./config.docker.yml /home/server/config.yml
COPY ./start.sh /home/server/start.sh
COPY ./notebook.sh /home/server/notebook.sh
COPY ./erica /home/server/erica
COPY ./commands /home/server/commands

RUN chown -R server:server /home/server

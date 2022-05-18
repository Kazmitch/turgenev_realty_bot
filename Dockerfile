FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    python3 python3-pip cron
ENV PYTHONUNBUFFERED 1
RUN mkdir /realty_tg_bot
COPY ./requirements.txt /realty_tg_bot/
COPY . /realty_tg_bot/
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /conf/requirements.txt
RUN pip3 freeze
WORKDIR /realty_tg_bot

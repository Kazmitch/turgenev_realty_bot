FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    python3 python3-pip cron libpangocairo-1.0-0
ENV PYTHONUNBUFFERED 1
RUN mkdir /turgenev_realty_bot
COPY ./requirements.txt /turgenev_realty_bot/
COPY . /turgenev_realty_bot/
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /turgenev_realty_bot/requirements.txt
RUN pip3 freeze
WORKDIR /turgenev_realty_bot

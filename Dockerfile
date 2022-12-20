FROM ubuntu:latest
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    python3 python3-pip cron libpangocairo-1.0-0

RUN apt-get install -y tzdata
RUN mkdir /realty_tg_bot
COPY ./requirements.txt /realty_tg_bot/
COPY . /realty_tg_bot/
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /realty_tg_bot/requirements.txt
RUN pip3 freeze
WORKDIR /realty_tg_bot

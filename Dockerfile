FROM ubuntu:bionic

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    curl unzip wget \
    xvfb firefox vim

RUN apt-get install dbus-x11

# install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz \
    && tar -x geckodriver -zf geckodriver-v0.23.0-linux64.tar.gz -O > /usr/local/bin/geckodriver \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v0.23.0-linux64.tar.gz

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install tzdata

RUN apt-get install make libc-dev gcc bash
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN rm -rf /requirements.txt

COPY src /src
WORKDIR /src

ENTRYPOINT "./scripts/entrypoint.sh"

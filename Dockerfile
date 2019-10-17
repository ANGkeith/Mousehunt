FROM ubuntu:bionic

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get clean \
    && apt-get update \
    && apt-get install --no-install-recommends -y\
        wget \
        dbus-x11 \
        dumb-init \
        tzdata \
        sox \
        pulseaudio \
        python3-pip \
        firefox \
        && rm -rf /var/lib/apt/lists/*

# install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz \
    && tar -x geckodriver -zf geckodriver-v0.23.0-linux64.tar.gz -O > /usr/local/bin/geckodriver \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v0.23.0-linux64.tar.gz

COPY requirements.txt /
RUN pip3 install --upgrade --user pip \
    && python3 -m pip install --user -r /requirements.txt \
    && rm -rf /requirements.txt

COPY src /src
WORKDIR /src

ENTRYPOINT ["/usr/bin/dumb-init", "./scripts/entrypoint.sh" ]

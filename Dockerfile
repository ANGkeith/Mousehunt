FROM python:3.7-alpine

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk update \
    && apk add --no-cache \
        bash \
        wget \
        dbus-x11 \
        dumb-init \
        firefox-esr \
        mesa-gl \
        mesa-dri-swrast \
        ttf-freefont \
        tzdata \
        sox

# install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz \
    && tar -x geckodriver -zf geckodriver-v0.23.0-linux64.tar.gz -O > /usr/local/bin/geckodriver \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v0.23.0-linux64.tar.gz

COPY requirements.txt /
RUN pip3 install --upgrade pip \
    &&  pip3 install -r /requirements.txt \
    && rm -rf /requirements.txt

COPY src /src
WORKDIR /src

ENTRYPOINT ["/usr/bin/dumb-init", "./scripts/entrypoint.sh" ]

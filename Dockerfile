FROM ubuntu:bionic

# Create user
RUN useradd -ms /bin/bash  bot

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get clean \
    && apt-get update \
    && apt-get install --no-install-recommends -y\
        wget \
        dbus-x11 \
        dumb-init \
        tzdata \
        python3-pip \
        python3-virtualenv \
        firefox \
        vim \
        firefox-geckodriver \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

# activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt /
RUN pip3 install --upgrade pip \
    && pip3 install -r /requirements.txt \
    && rm -rf /requirements.txt

COPY src /app
WORKDIR /app

RUN chown -R bot:bot /app
RUN chmod 777 /app
USER bot

# Update PATH
ENV PATH="/app/scripts:${PATH}"

# ENTRYPOINT ["/usr/bin/dumb-init", "./scripts/start_bot.sh" ]
ENTRYPOINT ["start_bot.sh"]

# default script to run
# CMD ["start_bot.sh" ]

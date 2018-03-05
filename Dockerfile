FROM ubuntu:bionic

LABEL maintainer="Khiem Doan <doankhiem.crazy@gmail.com>"

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8


# install web service
COPY requirements.txt /src/requirements.txt
COPY docker/http_task_scheduler.py /src/http_task_scheduler.py
RUN buildDeps='python3-pip' \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3 \
    && apt-get install -y --no-install-recommends $buildDeps \
    && pip3 install --upgrade pip --no-cache-dir \
    && pip3 install setuptools --no-cache-dir \
    && pip3 install gunicorn gevent --no-cache-dir \
    && pip3 install -r /src/requirements.txt --no-cache-dir \
    && apt-get purge -y --auto-remove $buildDeps \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# use for debug
ENV FLASK_APP /src/schedule_service.py
ENV FLASK_DEBUG 1


# install cron
RUN apt-get update \
    && apt-get -y install cron \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*


WORKDIR /src
EXPOSE 6000
ENTRYPOINT cron && gunicorn http_task_scheduler:app \
    --bind=0.0.0.0:6000 --workers=1 --worker-class=gevent
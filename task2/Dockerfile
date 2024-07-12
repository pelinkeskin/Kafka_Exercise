FROM python:3.12.4-bullseye


USER root

RUN python3 -m pip install beautifulsoup4
RUN python3 -m pip install requests
RUN python3 -m pip install confluent_kafka
RUN python3 -m pip install asyncio
RUN python3 -m pip install Flask
RUN python3 -m pip install gunicorn

ARG bootstrap_servers
ARG topic

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV bootstrap_servers=$bootstrap_servers
ENV topic=$topic

WORKDIR /task2
COPY . .

EXPOSE 8000
ENTRYPOINT [ "/bin/sh", "-c", "exec gunicorn -w 1 -b 0.0.0.0:8000 'main:app'" ]
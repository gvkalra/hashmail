# -*- coding: utf-8 -*-

#
#   celery worker -A tasks --workdir ./hashmail/ -l info -E
#
#

from os import environ
from celery import Celery
CLOUDAMQP_URL=environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2F?connection_attempts=3&heartbeat_interval=3600')

app = Celery('tasks', broker_url=CLOUDAMQP_URL)

@app.task(name='hashmail.tasks.echo')
def echo(x):
    x=x
    return "Your message has been processed Gau, your message is:::> %s "% x

@app.task(name='hashmail.tasks.add')
def add(x, y):
    return x + y

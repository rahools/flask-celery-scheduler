from celery import Celery
from time import sleep

app = Celery('tasks', broker = 'amqp://localhost')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30, reverse.s('hello'), name='add every 30')

@app.task
def reverse(text):
    sleep(5)
    return text[::-1]

def addTask():
    app.add_periodic_task(10, reverse.s('bye'), name='add every 10')
from flask import Flask
from celery import Celery
from time import sleep

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost'
app.config['CELERY_BROKER_HEARTBEAT'] = 0
app.config['CELERYBEAT_SCHEDULE'] = {}

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

##################################################
# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kargs):
#     sender.add_periodic_task(30, my_background_task.s(10, 10), name='add every 30')

@celery.task
def my_background_task(arg1, arg2):
    sleep(5)
    return arg1 + arg2



##################################################
@app.route('/', methods=['GET', 'POST'])
def index():
    celery.add_periodic_task(30, my_background_task.s(10, 10), name='add every 30')
    return 'hello?'





if __name__ == "__main__":
    app.run()
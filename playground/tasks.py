from time import sleep
from celery import shared_task

@shared_task
def notify_customer(message):
    print('sending 10 k emails')
    print(message)
    sleep(10)
    print('done sending 10 k emails')
import RPi.GPIO as IO
import time
from loguru import logger
import os
import requests
from components.own_camera import take_picture
from components.thread_util import execute_background

IO.setwarnings(False)
IO.setmode(IO.BOARD)
IO.setup(8, IO.IN)


def check_movements():
    logger.info('check_movements starting ..')
    while True:
        if(IO.input(8) == True):
            logger.info("Obstacle detected !!")
            take_picture()
            notify_by_picture()           
        else:
            time.sleep(0.4)


def notify_by_picture():
    logger.info("notify_by_picture !!")
    HOST = os.environ.get('API_SERVER_HOST') if 'API_SERVER_HOST' in os.environ else '127.0.0.1'
    logger.info("Host {0}",HOST)
    files = {'media': open('matricula.jpg', 'rb')}
    requests.post(HOST, files=files)

def start_sensor():
    execute_background(check_movements)
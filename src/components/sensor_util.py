import RPi.GPIO as IO
import time
from loguru import logger
import os
import requests
from src.components.own_camera import take_picture
from http import HTTPStatus

SLEEP_TIME = os.environ.get('SLEEP_TIME') if 'SLEEP_TIME' in os.environ else 1
PIN = os.environ.get('PIN') if 'PIN' in os.environ else 8


IO.setwarnings(False)
IO.setmode(IO.BOARD)
IO.setup(int(PIN), IO.IN)


def check_movements():
    logger.info('check_movements starting ..')
    while True:
        try:
            if(IO.input(8) == False):
                logger.info("Obstacle detected !!")
                take_picture()
                notify_by_picture()
                time.sleep(int(SLEEP_TIME))           
            time.sleep(int(SLEEP_TIME))
        except Exception as e:
            logger.info("Error looking out movements")
            logger.exception(e)
   


def notify_by_picture():
    logger.info("notify_by_picture !!")
    HOST = os.environ.get('API_SERVER_HOST') if 'API_SERVER_HOST' in os.environ else 'http://192.168.1.7:9090/raspberry/api/v1/accesos/registro-acceso-vehicular'
    logger.info("Host {0}",HOST)
    for index in range(3):
        try:
            files = {'file': open('matricula.jpg', 'rb')}
            response = requests.post(HOST, files=files)
            if(response.status_code == HTTPStatus.OK):
                logger.debug("Response\n"+ str(response.content))
                break
        except Exception as e:
                logger.exception(e)
    
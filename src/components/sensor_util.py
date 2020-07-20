import RPi.GPIO as IO
import time
from loguru import logger
import os
import requests
from src.components.own_camera import take_picture
from http import HTTPStatus

SLEEP_TIME = os.environ.get('SLEEP_TIME') if 'SLEEP_TIME' in os.environ else 1
PIN_SENSOR = os.environ.get('PIN_SENSOR') if 'PIN_SENSOR' in os.environ else 16
PIN_RED_LED = os.environ.get('PIN_RED_LED') if 'PIN_RED_LED' in os.environ else 10
PIN_BLUE_LED = os.environ.get('PIN_BLUE_LED') if 'PIN_BLUE_LED' in os.environ else 8


IO.setwarnings(False)
IO.setmode(IO.BOARD)
IO.setup(int(PIN_SENSOR), IO.IN)
IO.setup(int(PIN_SENSOR), IO.OUT)
IO.setup(int(PIN_SENSOR), IO.OUT)


def check_movements():
    logger.info('check_movements starting ..')
    while True:
        try:
            if(IO.input(PIN_SENSOR) == False):
                logger.info("Obstacle detected !!")
                take_picture()
                notify_by_picture()
                time.sleep(int(SLEEP_TIME))           
            time.sleep(int(SLEEP_TIME))
        except Exception as e:
            logger.info("Error looking out movements")
            logger.exception(e)

def access():
    IO.output(PIN_BLUE_LED,True)
    IO.output(PIN_RED_LED,False)
    time.sleep(2)
    IO.output(PIN_BLUE_LED,False)
    IO.output(PIN_RED_LED,True)   


def reset_status():
    IO.output(PIN_BLUE_LED,False)
    IO.output(PIN_RED_LED,True)   
    

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
    

reset_status()
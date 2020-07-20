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
HOST = os.environ.get('API_SERVER_HOST') if 'API_SERVER_HOST' in os.environ else 'http://192.168.1.7:9090/'
ACCESO_VEHICULAR_PATH = os.environ.get('ACCESO_VEHICULAR_PATH') if 'ACCESO_VEHICULAR_PATH' in os.environ else 'raspberry/api/v1/accesos/registro-acceso-vehicular'
ACCESO_PEATONAL_PATH = os.environ.get('ACCESO_PEATONAL_PATH') if 'ACCESO_PEATONAL_PATH' in os.environ else '/raspberry/api/v1/accesos/registro-acceso-peatonal'


IO.setwarnings(False)
IO.setmode(IO.BOARD)
IO.setup(int(PIN_SENSOR), IO.IN)
IO.setup(int(PIN_RED_LED), IO.OUT)
IO.setup(int(PIN_BLUE_LED), IO.OUT)


def check_movements():
    logger.info('check_movements starting ..')
    while True:
        try:
            if(IO.input(PIN_SENSOR) == False):
                logger.info("Obstacle detected !!")
                take_picture()
                notify_by_movement()
                time.sleep(int(SLEEP_TIME))           
            time.sleep(int(SLEEP_TIME))
        except Exception as e:
            logger.info("Error looking out movements")
            logger.exception(e)

def access():
    IO.output(PIN_BLUE_LED,True)
    IO.output(PIN_RED_LED,False)
    time.sleep(3)
    IO.output(PIN_BLUE_LED,False)
    IO.output(PIN_RED_LED,True)   


def reset_status():
    IO.output(PIN_BLUE_LED,False)
    IO.output(PIN_RED_LED,True)   
    

def notify_by_picture():
    logger.info("notify_by_picture !!")
    logger.info("Host {0}",HOST+ACCESO_VEHICULAR_PATH)
    for index in range(3):
        try:
            files = {'file': open('matricula.jpg', 'rb')}
            response = requests.post(HOST+ACCESO_VEHICULAR_PATH, files=files)
            if(response.status_code == HTTPStatus.OK):
                logger.debug("Response ok")
                break
        except Exception as e:
                logger.exception(e)

def notify_by_movement():
    logger.info("notify_by_picture !!")
    logger.info("Host {0}",HOST+ACCESO_PEATONAL_PATH)
    for index in range(3):
        try:
            response = requests.get(HOST)
            if(response.status_code == HTTPStatus.OK):
                logger.debug("Response ok")
                break
        except Exception as e:
                logger.exception(e)
        

reset_status()
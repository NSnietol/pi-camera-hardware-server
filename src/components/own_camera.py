from time import sleep
from picamera import PiCamera
from loguru import logger
import os
SLEEP_TIME = os.environ.get('SLEEP_TIME') if 'SLEEP_TIME' in os.environ else 1


def take_picture():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    logger.info("Camera setting ok")
    camera.start_preview()
    # Camera warm-up time
    remove_old_file()
    sleep(int(SLEEP_TIME))
    camera.capture('matricula.jpg')
    logger.info("it took the picture")
    camera.close()

def remove_old_file():
    if( os.path.exists('matricula.jpg')):
        os.remove('matricula.jpg')


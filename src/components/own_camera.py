from time import sleep
from picamera import PiCamera
from loguru import logger
import os


def take_picture():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    logger.info("Camera setting ok")
    camera.start_preview()
    # Camera warm-up time
    remove_old_file()
    sleep(1)
    camera.capture('matricula.jpg')
    logger.info("it took the picture")
    camera.close()

def remove_old_file():
    if( os.path.exists('matricula.jpg')):
        os.remove('matricula.jpg')


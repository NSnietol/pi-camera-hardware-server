from time import sleep
from picamera import PiCamera
from loguru import logger


def take_picture():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    logger.info("Camera setting ok")
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture('matricula.jpg')
    logger.info("it took the picture")
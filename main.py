
import os
from fastapi import FastAPI, HTTPException,BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn
import threading
import time

from src.components.own_camera import take_picture
from fastapi.responses import FileResponse
from src.components.sensor_util import check_movements


def settings():
    HOST = os.environ.get(
        'API_HOST') if 'API_HOST' in os.environ else '127.0.0.1'
    PORT = os.environ.get('API_PORT') if 'API_PORT' in os.environ else '9090'
    ORIGIN_ALLOWED = os.environ.get(
        'ORIGIN_ALLOWED') if 'ORIGIN_ALLOWED' in os.environ else '*'

    logger.info(PORT)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[ORIGIN_ALLOWED],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app = FastAPI()
settings()


@app.get("/get-picture/")
async def get_picture_controller():
    logger.info("Picture in progress ...")
    take_picture()
    return FileResponse('matricula.jpg')

@app.get("/unlock/")
async def unlock_door():
    logger.info("Opening door in progress ...")
    return {"message": "Door opened"}

@app.get("/")
async def main():
    content = """
                <html>
                <head></head>
                <body>
                <h3>PiCamera Server Running ;)</h3>
              
                </body>
                
                </html>
             
                    """
    return HTMLResponse(content=content)


if __name__ == '__main__':
    x = threading.Thread(target=check_movements)
    x.start()
    logger.info('uvicorn')
    uvicorn.run(app)
    logger.info('End')



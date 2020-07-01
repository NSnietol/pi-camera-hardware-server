
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.components.camera import take_picture
from fastapi.responses import FileResponse


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
    return FileResponse('src/components/matricula.jpg')



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

# import string
#
# from fastapi import FastAPI
#
# from app.core.config import PROJECT_NAME, HOST, PORT
# from app.utils import setup
from datetime import time
from time import sleep

# app = FastAPI(title=f"{PROJECT_NAME}")
# setup(app)


while True:
    sleep(1000)

# @app.get("/",
#          summary="Статус API",
#          description="Проверка работы API",
#          response_description=f'Возвращает "{PROJECT_NAME} работает!"'
#          )
# async def root():
#     return {"message": f"{PROJECT_NAME} работает!"}
#
#
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run("main:app", host=HOST, port=PORT, reload=True)

from fastapi import FastAPI

from app.core.config import PROJECT_NAME
from app.utils import setup

app = FastAPI(title=f"{PROJECT_NAME}")
setup(app)


@app.get("/",
         summary="Статус API",
         description="Проверка работы API",
         response_description=f'Возвращает "{PROJECT_NAME} работает!"'
         )
async def root():
    return {"message": f"{PROJECT_NAME} работает!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

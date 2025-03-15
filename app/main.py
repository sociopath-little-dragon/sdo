# sdo project
from uvicorn import run
from fastapi import FastAPI, APIRouter
from app.config.config import init_config
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router as app_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно настроить конкретные источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP-методы
    allow_headers=["*"],  # Разрешить все заголовки
)

def main():
    app.include_router(app_router)  # include all routers

    cfg = init_config()  # load config

    run(app, host=cfg['app']['host'], port=cfg['app']['port'])  # run app

if __name__ == '__main__':
    main()

# система очередей для тестирования
# изменение бд
# добавление лаб студентов для преподов, добавление тестов
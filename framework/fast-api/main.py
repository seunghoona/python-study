from fastapi import FastAPI
from .routers import users, items

app = FastAPI()

# 라우터 등록
app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

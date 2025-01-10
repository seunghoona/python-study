from fastapi import FastAPI
from utils import test
from uvicorn import run
from routers import member
app = FastAPI()

app.include_router(member.router)


@app.get("/")
def read_root():
    return test.items()


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)

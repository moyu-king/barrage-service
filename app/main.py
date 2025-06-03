from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "status": 1,
        "message": 'ok',
        "data": {"Hello": "World"}
    }

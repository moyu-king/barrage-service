from fastapi import FastAPI
from app.service.tencent import get_tencent_barrage

app = FastAPI()


@app.get("/")
async def get_barrage():
    return await get_tencent_barrage()

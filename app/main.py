from fastapi import FastAPI
from app.service.tencent import get_tencent_barrage, get_tencent_episodes

app = FastAPI()


@app.get("/episode")
async def get_episodes():
    return await get_tencent_episodes()


@app.get("/barrage")
async def get_barrage():
    return await get_tencent_barrage()

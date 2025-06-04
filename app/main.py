from fastapi import FastAPI
from app.service.tencent import get_tencent_barrages, get_tencent_episodes
from app.models.video import Video, db

from app.service.tencent import tencent_router

app = FastAPI()


#路由分组
app.include_router(tencent_router, prefix="/tencent", tags=["腾讯接口"])
# app.include_router(bilibili.router, prefix="/bilibili", tags=["B战接口"])


# @app.get("/episodes")
# async def get_episodes():
#     return await get_tencent_episodes()

# @app.get("/barrages")
# async def get_barrages():
#     return await get_tencent_barrages()

@app.get("/videos")
async def get_videos():
    with db.connection_context():
        return list(Video.select().dicts())

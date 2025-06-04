from fastapi import FastAPI
from app.models.video import Video, db
from app.service.tencent import tencent_router

app = FastAPI()


# 路由分组
app.include_router(tencent_router, prefix="/tencent", tags=["腾讯接口"])
# app.include_router(bilibili.router, prefix="/bilibili", tags=["B战接口"])

@app.get("/videos")
async def get_videos():
    with db.connection_context():
        return list(Video.select().dicts())

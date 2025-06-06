from fastapi import FastAPI
from app.models.video import Video, db
from app.service.tencent import tencent_router
from app.models.resp import JsonResponse

app = FastAPI()


# 路由分组
app.include_router(tencent_router, prefix="/tencent", tags=["腾讯接口"])
# app.include_router(bilibili.router, prefix="/bilibili", tags=["B战接口"])

@app.get("/videos")
async def get_videos():
    try:
        with db.connection_context():
            return JsonResponse.success(data=list(Video.select().dicts()))
    except Exception:
        return JsonResponse.fail(message="服务器内部错误")

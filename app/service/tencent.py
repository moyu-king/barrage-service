from typing import Union
from fastapi import APIRouter
from pydantic import BaseModel
from app.service.DanmuFetcher import DanmuFetcher
from app.service.EpisodeFetcher import EpisodeFetcher
from app.models.resp import JsonResponse

tencent_router = APIRouter()

class EpisodePayload(BaseModel):
    cid: Union[str, None]
    vid: Union[str, None]
    pageContext: Union[str, None] = None

# 获取弹幕
# duration 视频时长
@tencent_router.get("/barrage")
async def tencent_barrage(duration: int):
    try:
        fetcher = DanmuFetcher()
        # 获取所有弹幕
        danmus = await fetcher.fetch_all(duration * 2)
        if not danmus:
            return JsonResponse.fail(messge='弹幕数据获取失败')

        barrage_list = [item for sublist in danmus for item in sublist]
        return JsonResponse.success(messge='成功', data=barrage_list)
    except Exception:
        return JsonResponse.fail(messge='弹幕数据获取异常')


# 获取集数
@tencent_router.post("/episode")
async def tencent_episodes(payload: EpisodePayload):
    try:
        fetcher = EpisodeFetcher()
        
        # 获取所有集数
        data = await fetcher.fetch_all(payload.cid, payload.vid)
        if not data:
            return JsonResponse.fail(messge='集数数据获取失败')
        
        episode_list = [item for sublist in data for item in sublist]
        return JsonResponse.success(messge='成功', data=episode_list)
    except Exception:
        return JsonResponse.fail(messge='集数数据获取异常')


from typing import Union
from fastapi import APIRouter
from pydantic import BaseModel
from app.service.DanmuFetcher import DanmuFetcher
from app.service.EpisodeFetcher import EpisodeFetcher
from app.models.resp import JsonResponse
from app.models.video import Video

tencent_router = APIRouter()


class EpisodePayload(BaseModel):
    cid: Union[str, None]
    vid: Union[str, None]
    pageContext: Union[str, None] = None


"""
获取弹幕
    duration 视频时长
    vid
    filter 是否过滤弹幕 true | false
"""

@tencent_router.get("/barrage")
async def tencent_barrage(duration: int, vid: str, filter: bool):
    try:
        fetcher = DanmuFetcher()
        # 获取所有弹幕
        danmus = await fetcher.fetch_all(duration * 2, vid, filter)
        if not danmus:
            return JsonResponse.fail(message="弹幕数据获取失败")

        barrage_list = [item for sublist in danmus for item in sublist]
        return JsonResponse.success(message="成功", data=barrage_list)
    except Exception:
        return JsonResponse.fail(message="弹幕数据获取异常")


# 获取集数
@tencent_router.get("/episode/{id}")
async def tencent_episodes(id: int):
    try:
        video = Video.get_or_none(Video.id == id)
        if not video:
            return JsonResponse.fail(message="无效视频id")

        fetcher = EpisodeFetcher()
        # 获取所有集数
        params = video.params
        data = await fetcher.fetch_all(params["cid"], params["vid"])
        if not data:
            return JsonResponse.fail(message="集数数据获取失败")

        episode_list = [item for sublist in data for item in sublist]
        return JsonResponse.success(message="成功", data=episode_list)
    except Exception:
        return JsonResponse.fail(message="集数数据获取异常")

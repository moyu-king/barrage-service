from fastapi import APIRouter
from app.service.tencent_episode_fetcher import TencentEpisodeFetcher
from app.service.tencent_barrage_fetcher import TencentBarrageFetcher
from app.models.resp import JsonResponse
from app.models.video import Video

tencent_router = APIRouter()

"""
获取弹幕
    duration 视频时长
    vid
    filter 是否过滤弹幕 true | false
"""

@tencent_router.get("/barrage")
async def tencent_barrage(duration: int, vid: str, filter: bool):
    try:
        fetcher = TencentBarrageFetcher()
        # 获取所有弹幕
        barrages = await fetcher.fetch_all(duration * 2, vid, filter)
        if not barrages:
            return JsonResponse.fail(message="弹幕数据获取失败")

        barrage_list = [item for sublist in barrages for item in sublist]
        return JsonResponse.success(message="成功", data=barrage_list)
    except Exception:
        return JsonResponse.fail(message="弹幕数据获取异常")


# 获取集数
@tencent_router.get("/episode")
async def tencent_episodes(vid: int):
    try:
        video = Video.get_or_none(Video.id == vid)
        if not video:
            return JsonResponse.fail(message="无效视频id")

        fetcher = TencentEpisodeFetcher()
        # 获取所有集数
        params = video.params
        data = await fetcher.fetch_all(params["cid"], params["vid"])
        if not data:
            return JsonResponse.fail(message="集数数据获取失败")

        episode_list = [item for sublist in data for item in sublist]
        return JsonResponse.success(message="成功", data=episode_list)
    except Exception:
        return JsonResponse.fail(message="集数数据获取异常")

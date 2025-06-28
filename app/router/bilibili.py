from fastapi import APIRouter
from app.service.bilibili_barrage_fetcher import BiliBiliBarrageFetcher
from app.service.bilibili_episode_fetcher import BiliBiliEpisodeFetcher
from app.models.resp import JsonResponse
from app.models.video import Video

bilibili_router = APIRouter()

@bilibili_router.get('/barrage')
async def bilibili_barrage(duration: int, vid: str, filter: bool):
    fetcher = BiliBiliBarrageFetcher()
    barrages = await fetcher.fetch_all(duration, vid, filter)

    if not barrages:
        return JsonResponse.fail(message="弹幕数据获取失败")
    else:
        return JsonResponse.success(message="成功", data=barrages)

@bilibili_router.get('/episode')
async def bilibili_episodes(vid: int):
    video = Video.get_or_none(Video.id == vid)

    if not video:
        return JsonResponse.fail(message="无效视频id")

    fetcher = BiliBiliEpisodeFetcher()
    episodes = await fetcher.fetch_all(video.params)
    if not episodes:
        return JsonResponse.fail(message="集数数据获取失败")
    else:
        return JsonResponse.success(message="成功", data=episodes)

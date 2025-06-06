from aiohttp import ClientSession
from typing import Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service.DanmuFetcher import DanmuFetcher

tencent_router = APIRouter()

class EpisodePayload(BaseModel):
    cid: Union[str, None]
    vid: Union[str, None]
    pageContext: Union[str, None] = None

# 获取弹幕
# duration 视频时长
@tencent_router.post("/barrage")
async def tencent_barrage(duration: int):
    try:
        fetcher = DanmuFetcher()
        # 获取所有弹幕
        danmus = await fetcher.fetch_all(duration * 2)
        if not danmus:
            raise HTTPException(status_code=500, detail="弹幕数据获取失败")
        # 后续再优化统一返回格式
        return danmus
    except Exception:
        raise HTTPException(status_code=404, detail="弹幕数据获取失败")


# 获取集数
@tencent_router.post("/episode")
async def tencent_episodes(payload: EpisodePayload):
    async with ClientSession() as session:
        baseUrl = "https://pbaccess.video.qq.com/trpc.universal_backend_service.page_server_rpc.PageServer/GetPageData"
        headers = {"referer": "https://v.qq.com"}
        params = {"video_appid": "3000010", "vplatform": 2, "vversion_name": "8.2.96"}
        json = {
            "page_params": {
                "req_from": "web_vsite",
                "page_id": "vsite_episode_list",
                "page_type": "detail_operation",
                "id_type": "1",
                "cid": payload.cid,
                "vid": payload.vid,
                "lid": "",
                "page_num": "",
                "detail_page_type": "1",
                "page_context": payload.pageContext
            },
            "has_cache": 1
        }

        response = await session.post(baseUrl, headers=headers, params=params, json=json)

        return episode_response(await response.json(), payload.pageContext)


# 集数
def episode_response(response):
    json_data = {}
    episodes = []

    module_list_data = response['data']['module_list_datas'][0]
    item_datas = module_list_data['module_datas'][0]['item_data_lists']['item_datas']

    for item in item_datas:
        item_params = item['item_params']

        if 'cid' in item_params:
            episode = {}
            episode['cid'] = item_params['cid']
            episode['vid'] = item_params['vid']
            episode['union_title'] = item_params['union_title']
            episode['title'] = item_params['title']
            episodes.append(episode)

    json_data['data'] = episodes

    return json_data

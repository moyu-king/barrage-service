from aiohttp import ClientSession
from typing import Union
from fastapi import APIRouter
 
tencent_router  = APIRouter()

# https://dm.video.qq.com/barrage/segment/e0018sdzesg/t/v1/390000/420000
# 获取弹幕
@tencent_router.post("/barrage")
async def tencent_barrage(time_offset1: str, time_offset2: str):
    async with ClientSession() as session:
        
        response = await session.get("https://dm.video.qq.com/barrage/segment/e0018sdzesg/t/v1/" + time_offset1 + "/" + time_offset2)
        return barrage_response(await response.json())



# 获取集数
@tencent_router.post("/episode")
async def tencent_episodes(cid: Union[str, None], vid: Union[str, None], pageContext: Union[str, None]):
    async with ClientSession() as session:
        baseUrl = "https://pbaccess.video.qq.com/trpc.universal_backend_service.page_server_rpc.PageServer/GetPageData"
        headers = {"referer": "https://v.qq.com"}
        params = {"video_appid": "3000010", "vplatform": 2, "vversion_name": "8.2.96"}
        payload = {
            "page_params": {
                "req_from": "web_vsite",
                "page_id": "vsite_episode_list",
                "page_type": "detail_operation",
                "id_type": "1",
                "cid": cid,
                "vid": vid,
                "lid": "",
                "page_num": "",
                "detail_page_type": "1",
                "page_context": pageContext
            },
            "has_cache": 1
        }

        response = await session.post(baseUrl, headers=headers, params=params, json=payload)

        return episode_response(await response.json(), pageContext)



# 弹幕
def barrage_response(response):

    json_data = {}
    json_txt = {
        'barrages': []
    }
    json_data['data'] = json_txt
    barrages = []
    
    items = response['barrage_list']
    for item in items:
        barrage = {}
        barrage['time_offset'] = item['time_offset']
        barrage['content'] = item['content']
        barrages.append(barrage)

    json_txt['barrages'] = barrages
    return json_data

# 集数
def episode_response(response, pageContext):

    json_data = {}
    json_txt = {}
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

    json_txt['barrages'] = episodes
    json_data['data'] = json_txt
    json_data['pageContext'] = pageContext
    return json_data



async def get_tencent_barrages():
    async with ClientSession() as session:
        response = await session.get("https://dm.video.qq.com/barrage/segment/e0018sdzesg/t/v1/390000/420000")
        return await response.json()


async def get_tencent_episodes():
    async with ClientSession() as session:
        baseUrl = "https://pbaccess.video.qq.com/trpc.universal_backend_service.page_server_rpc.PageServer/GetPageData"
        headers = {"referer": "https://v.qq.com"}
        params = {"video_appid": "3000010", "vplatform": 2, "vversion_name": "8.2.96"}
        payload = {
            "page_params": {
                "req_from": "web_vsite",
                "page_id": "vsite_episode_list",
                "page_type": "detail_operation",
                "id_type": "1",
                "cid": "mcv8hkc8zk8lnov",
                "vid": "x0036x5qqsr",
                "detail_page_type": "1",
                "page_context": ""
            },
            "has_cache": 1
        }

        response = await session.post(baseUrl, headers=headers, params=params, json=payload)

        return await response.json()

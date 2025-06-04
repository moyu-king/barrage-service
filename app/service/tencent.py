from aiohttp import ClientSession


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

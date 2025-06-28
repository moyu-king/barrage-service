import asyncio
import re
from aiohttp import ClientSession
from app.service.interface import EpisodeFetcher

class TencentEpisodeFetcher(EpisodeFetcher):
    BASE_URL = "https://pbaccess.video.qq.com/trpc.universal_backend_service.page_server_rpc.PageServer/GetPageData"
    HEADERS = {"referer": "https://v.qq.com"}
    PARAMS = {"video_appid": "3000010", "vplatform": 2, "vversion_name": "8.2.96"}
    CID = ""
    VID = ""
    PAGE_NUM = 30

    async def fetch_all(self, cid, vid):
        self.CID = cid
        self.VID = vid

        # 获取所有分页参数
        pageContext_list = await self.get_pageContext()

        # 批量获取集数
        tasks = [self.fetch_one(pageContext) for pageContext in pageContext_list]
        return await asyncio.gather(*tasks)

    """'
    获取所有集数
    """

    async def fetch_one(self, pageContext):
        async with ClientSession() as session:
            try:
                json = {
                    "page_params": {
                        "req_from": "web_vsite",
                        "page_id": "vsite_episode_list",
                        "page_type": "detail_operation",
                        "id_type": "1",
                        "cid": self.CID,
                        "vid": self.VID,
                        "lid": "",
                        "page_num": "",
                        "detail_page_type": "1",
                        "page_context": pageContext["page_context"],
                    },
                    "has_cache": 1,
                }

                async with session.post(
                    self.BASE_URL, headers=self.HEADERS, params=self.PARAMS, json=json
                ) as resp:

                    response = await resp.json()
                    episodes = []

                    module_list_data = response["data"]["module_list_datas"][0]
                    item_datas = module_list_data["module_datas"][0]["item_data_lists"]["item_datas"]

                    for item in item_datas:
                        item_params = item["item_params"]

                        if "cid" in item_params:
                            episode = {}
                            episode["vid"] = item_params["vid"]
                            episode["union_title"] = item_params["union_title"]
                            episode["title"] = item_params["title"]
                            episode["duration"] = int(item_params["duration"]) * 1000  # 统一转成ms
                            episode["season"] = pageContext["season"]
                            episodes.append(episode)

                    return episodes
            except Exception:
                return []

    """'
    获取分页参数
    """

    async def get_pageContext(self):
        async with ClientSession() as session:
            try:
                json = {
                    "page_params": {
                        "req_from": "web_vsite",
                        "page_id": "vsite_episode_list",
                        "page_type": "detail_operation",
                        "id_type": "1",
                        "cid": self.CID,
                        "vid": self.VID,
                        "lid": "",
                        "page_num": "",
                        "detail_page_type": "1",
                        "page_context": "",
                    },
                    "has_cache": 1,
                }

                async with session.post(
                    self.BASE_URL, headers=self.HEADERS, params=self.PARAMS, json=json
                ) as resp:

                    response = await resp.json()
                    page_context_list = []
                    module_data = response["data"]["module_list_datas"][0]["module_datas"][0]
                    tabs = module_data["module_params"]["tabs"]

                    if tabs:
                        # 不分季度
                        page_context_list = [{"page_context": item, "season": ''} for item in re.findall('page_context":"(.*?)",', tabs)]
                    else:
                        # 分季度
                        item_datas = module_data["item_data_lists"]["item_datas"]

                        for item in item_datas:
                            params = item["item_params"]
                            if params and params.get("page_context"):
                                page_context_list.append({"page_context": params["page_context"], "season": params["title"]})

                    return page_context_list
            except Exception:
                return []

import asyncio
import re
from aiohttp import ClientSession
from typing import Union


class EpisodeFetcher:
    BASE_URL = "https://pbaccess.video.qq.com/trpc.universal_backend_service.page_server_rpc.PageServer/GetPageData"
    HEADERS = {"referer": "https://v.qq.com"}
    PARAMS = {"video_appid": "3000010", "vplatform": 2, "vversion_name": "8.2.96"}
    CID = ""
    VID = ""
    PAGE_NUM = 30


    async def fetch_all(self, cid, vid):

        self.CID = cid
        self.VID = vid

        # 获取总集数
        total_episodes = await self.get_total_episode()
        countFor = ""
        if int(total_episodes) % self.PAGE_NUM == 0:
            countFor = int(total_episodes) // self.PAGE_NUM
        else:
            countFor = int(total_episodes) // self.PAGE_NUM + 1

        # 批量获取集数
        tasks = [self.get_episode(num) for num in range(countFor)]
        return await asyncio.gather(*tasks)



    ''''
    获取所有集数
        num = 第几页
    '''
    async def get_episode(self, num):
        async with ClientSession() as session:
            try:
                pageContext = ""
                
                if num != 0:
                    episode_begin = self.PAGE_NUM * num + 1
                    episode_end = self.PAGE_NUM * (num + 1)
                    pageContext = f"chapter_name=&cid={self.CID}&detail_page_type=1&episode_begin={episode_begin}&episode_end={episode_end}&episode_step={self.PAGE_NUM}&filter_rule_id=&id_type=1&is_nocopyright=false&is_skp_style=false&lid=&list_page_context=&mvl_strategy_id=&need_tab=1&order=&page_num={num}&page_size={self.PAGE_NUM}&req_from=web_vsite&req_from_second_type=&req_type=0&siteName=&tab_type=1&title_style=&ui_type=null&un_strategy_id=13dc6f30819942eb805250fb671fb082&watch_together_pay_status=0&year="
                
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
                        "page_context": pageContext
                    },
                    "has_cache": 1
                }

                async with session.post(self.BASE_URL, headers=self.HEADERS, params=self.PARAMS, json=json) as resp:

                    response = await resp.json()
                    episodes = []

                    module_list_data = response["data"]["module_list_datas"][0]
                    item_datas = module_list_data["module_datas"][0]["item_data_lists"]["item_datas"]
                    for item in item_datas:
                        item_params = item["item_params"]

                        if "cid" in item_params:
                            episode = {}
                            episode["cid"] = item_params["cid"]
                            episode["vid"] = item_params["vid"]
                            episode["union_title"] = item_params["union_title"]
                            episode["title"] = item_params["title"]
                            episode["duration"] = item_params["duration"]
                            episodes.append(episode)

                    return episodes
            except Exception:
                return []
            

    ''''
    获取总集数
    '''
    async def get_total_episode(self):
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
                        "page_context": ""
                    },
                    "has_cache": 1
                }

                async with session.post(self.BASE_URL, headers=self.HEADERS, params=self.PARAMS, json=json) as resp:

                    response = await resp.json()
                    # "sub_title": "VIP用户每周五10点更新1集，SVIP用户限时福利抢先1天看1集（每周四18:00）/更新至218集"
                    sub_title = response["data"]["module_list_datas"][0]["module_datas"][0]["module_params"]["sub_title"]
                    count = re.findall("更新至(.*?)集", sub_title)
                    return count[0]
            except Exception:
                return []

import asyncio
from aiohttp import ClientSession
from app.service.interface import BarrageFetcher, BarrageField


class TencentBarrageFetcher(BarrageFetcher):
    # 间隔时间30秒
    TIME_OFFSET = 30000
    CONTENT_SCORE = 50
    '''
        duration: min
    '''
    async def fetch_all(self, duration, vid, filter):
        # 获取各个时间点
        timestamps = [i * self.TIME_OFFSET for i in range(duration * 2)]
        # 批量获取弹幕
        tasks = [self.fetch_one(time_end, vid, filter) for time_end in timestamps]
        return await asyncio.gather(*tasks)

    async def fetch_one(self, time_end: str, vid: str, filter: bool):
        async with ClientSession() as session:
            try:
                BASE_URL = f"https://dm.video.qq.com/barrage/segment/{vid}/t/v1"
                time_begin = time_end + self.TIME_OFFSET
                async with session.get(f"{BASE_URL}/{time_end}/{time_begin}") as resp:
                    response = await resp.json()
                    barrages = []

                    items = response["barrage_list"]
                    for item in items:
                        # 过滤 弹幕评分低于CONTENT_SCORE， 单字
                        if filter:
                            score = int(item["content_score"])
                            content = item["content"]
                            if score < self.CONTENT_SCORE or len(content) <= 1:
                                continue
                        barrage: BarrageField = {}
                        barrage["style"] = item["content_style"]
                        barrage["weight"] = item["content_score"]
                        barrage["offset"] = int(item["time_offset"])
                        barrage["content"] = item["content"]
                        barrages.append(barrage)

                    return barrages
            except Exception:
                return []

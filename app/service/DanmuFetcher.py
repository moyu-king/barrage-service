import asyncio
from aiohttp import ClientSession


class DanmuFetcher:
    
    # 间隔时间30秒
    TIME_OFFSET = 30000
    CONTENT_SCORE = 50

    async def fetch_all(self, duration: int, vid: str, filter: bool):
        # 获取各个时间点
        timestamps = [i * self.TIME_OFFSET for i in range(duration)]
        # 批量获取弹幕
        tasks = [self.get_danmu(time_end, vid, filter) for time_end in timestamps]
        return await asyncio.gather(*tasks)

    async def get_danmu(self, time_end: str, vid: str, filter: bool):
        async with ClientSession() as session:
            try:
                BASE_URL = f"https://dm.video.qq.com/barrage/segment/{vid}/t/v1"
                time_begin = time_end + self.TIME_OFFSET
                async with session.get(
                    f"{BASE_URL}/{time_end}/{time_begin}"
                ) as resp:
                    response = await resp.json()
                    barrages = []

                    items = response["barrage_list"]
                    for item in items:
                        # 过滤 弹幕评分低于CONTENT_SCORE， 单字
                        if filter:
                            score = int(item["content_score"])
                            content = item["content"]
                            if score < self.CONTENT_SCORE or len(content) <=1:
                                continue
                        barrage = {}
                        barrage["up_count"] = item["up_count"]
                        barrage["content_style"] = item["content_style"]
                        barrage["content_score"] = item["content_score"]
                        barrage["time_offset"] = item["time_offset"]
                        barrage["content"] = item["content"]
                        barrages.append(barrage)

                    return barrages
            except Exception:
                return []


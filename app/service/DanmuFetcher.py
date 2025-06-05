import asyncio 
from aiohttp import ClientSession

class DanmuFetcher:
    BASE_URL = "https://dm.video.qq.com/barrage/segment/e0018sdzesg/t/v1"
    # 间隔时间30秒
    TIME_OFFSET = 30000

    async def fetch_all(self, duration: int):
        # 获取各个时间点
        timestamps = [ i * self.TIME_OFFSET for i in range(duration) ]
        # 批量获取弹幕
        tasks = [self.get_danmu(time_end) for time_end in timestamps]
        return await asyncio.gather(*tasks)
    

    async def get_danmu(self, time_end: str):
        async with ClientSession() as session:
            try:
                time_begin = (time_end + self.TIME_OFFSET)
                async with session.get(
                    f"{self.BASE_URL}/{time_end}/{time_begin}"
                ) as resp:
                    response = await resp.json()
                    

                    # 直接调组装返回报文方法，但报错，后续再研究
                    # return await self.barrage_response(response)

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
            except Exception as e:
                return ["弹幕数据获取异常"]


    

    # 弹幕组装返回报文
    async def barrage_response(response):
        print(f"----------response：{response}")
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

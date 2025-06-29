import math
import random
import asyncio
from app.service.interface import BarrageFetcher
from aiohttp import ClientSession
from app.proto.barrage_pb2 import BarrageSegMobi1eReply
from app.constant import USER_AGENTS

class BiliBiliBarrageFetcher(BarrageFetcher):
    BASE_URL = "https://api.bilibili.com/x/v2/dm/web/seg.so"

    """
        duration: 视频总时长, b站的单位为ms
        vid: 视频的cid
        filter: 过滤垃圾弹幕
    """
    async def fetch_all(self, duration, vid, filter):
        segments = math.ceil(duration / (1000 * 60 * 6))
        tasks = [self.fetch_one(vid, index, filter) for index in range(1, segments + 1)]

        datas = await asyncio.gather(*tasks)
        return [item for data in datas for item in data]

    """
        segment_index: 弹幕片段, 6min一包, 从1开始
    """
    async def fetch_one(self, vid, segment_index: int, filter):
        async with ClientSession() as session:
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            params = {"oid": vid, "segment_index": segment_index, "type": 1}

            async with session.get(self.BASE_URL, headers=headers, params=params) as resp:
                protobuf = await resp.read()
                reply = BarrageSegMobi1eReply()
                reply.ParseFromString(protobuf)
                data = []

                for elem in reply.elems:
                    data.append({
                        "content": elem.content,
                        "style": f"color:#{hex(elem.color)[2:]}",
                        "offset": elem.progress,
                        "weight": elem.weight
                    })
                return data

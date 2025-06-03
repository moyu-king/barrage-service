from aiohttp import ClientSession


async def get_tencent_barrage():
    async with ClientSession() as session:
        response = await session.get('https://dm.video.qq.com/barrage/segment/e0018sdzesg/t/v1/390000/420000')
        return await response.json()

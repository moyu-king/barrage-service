from app.service.interface import EpisodeFetcher, EpisodeField
from typing import TypedDict
from aiohttp import ClientSession
from fake_useragent import UserAgent

class FetchParam(TypedDict, total=False):
    season_id: int
    ep_id: int


class BiliBiliEpisodeFetcher(EpisodeFetcher):
    BASE_URL = "https://api.bilibili.com/pgc/view/web/season"

    async def fetch_all(self, params: FetchParam):
        season_id = params.get("season_id")
        ep_id = params.get("ep_id")

        try:
          async with ClientSession() as session:
              params = {"season_id": season_id} if season_id else {"ep_id": ep_id}
              ua = UserAgent()
              headers = {"User-Agent": ua.random}

              async with session.get(self.BASE_URL, params=params, headers=headers) as resp:
                  response = await resp.json()
                  result = response["result"]
                  episodes: list[EpisodeField] = [{
                      "vid": item["cid"],  # B站的弹幕请需要cid，故将cid作为vid返回
                      "duration": item["duration"],
                      "season": "",
                      "title": item["title"],
                      "union_title": item["show_title"]} for item in result["episodes"]]

                  return episodes
        except Exception:
            return []

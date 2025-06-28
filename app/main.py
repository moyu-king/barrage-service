from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.router import tencent_router, bilibili_router, video_router
from app.constant import Platform
from aiohttp import ClientSession
from app.models.resp import JsonResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 路由分组
app.include_router(tencent_router, prefix="/tencent", tags=["腾讯接口"])
app.include_router(bilibili_router, prefix="/bilibili", tags=["bilibili接口"])
app.include_router(video_router, prefix="/video", tags=["视频接口"])


@app.api_route("/proxy/{path}", methods=["GET", "POST", "PUT", "DElETE"])
async def proxy_router(request: Request, path: str, platform: int):
    platform_path_map = {
        Platform.TENCENT.value: 'tencent',
        Platform.BILIBILI.value: 'bilibili'
    }

    try:
        async with ClientSession() as session:
            async with session.request(
                method=request.method,
                url=f"{request.base_url}{platform_path_map[platform]}/{path}",
                headers=dict(request.headers),
                params=dict(request.query_params),
                data=await request.body()
            ) as resp:
                return await resp.json()
    except Exception as e:
        return JsonResponse.fail(message=e)

if __name__ == "__main__":
    import uvicorn
    import sys
    import logging

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    try:
        logging.info("正在启动弹幕服务...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        logging.error(f"Failed to start server: {e}", exc_info=True)
        input("Press Enter to exit...")

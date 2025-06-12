from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.video import Video, db
from app.service.tencent import tencent_router
from app.models.resp import JsonResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 允许的方法
    allow_headers=["*"],
    expose_headers=["*"]
)

# 路由分组
app.include_router(tencent_router, prefix="/tencent", tags=["腾讯接口"])
# app.include_router(bilibili.router, prefix="/bilibili", tags=["B战接口"])

@app.get("/videos")
async def get_videos():
    try:
        with db.connection_context():
            return JsonResponse.success(data=list(Video.select().dicts()))
    except Exception:
        return JsonResponse.fail(message="服务器内部错误")


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
        logging.info("Starting FastAPI server...")
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

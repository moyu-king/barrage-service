from fastapi import APIRouter
from app.models.video import Video, db
from app.models.resp import JsonResponse
from pydantic import BaseModel

class VideoCreateOption(BaseModel):
    name: str
    params: str
    platform: int


video_router = APIRouter()

@video_router.get("/all")
async def get_videos():
    try:
        with db.connection_context():
            return JsonResponse.success(data=list(Video.select().dicts()))
    except Exception:
        return JsonResponse.fail(message="服务器内部错误")

@video_router.post("/")
async def create_video(opt: VideoCreateOption):
    try:
        with db.connection_context():
            video = Video.create(
                name=opt.name,
                params=opt.params,
                platform=opt.platform
            )

            return JsonResponse.success(data=video.__data__)
    except Exception as e:
        print(f"Video创建失败: {str(e)}")
        JsonResponse.fail('创建失败')

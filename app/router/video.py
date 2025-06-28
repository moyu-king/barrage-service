from fastapi import APIRouter
from app.models.video import Video, db
from app.models.resp import JsonResponse

video_router = APIRouter()

@video_router.get("/all")
async def get_videos():
    try:
        with db.connection_context():
            return JsonResponse.success(data=list(Video.select().dicts()))
    except Exception:
        return JsonResponse.fail(message="服务器内部错误")

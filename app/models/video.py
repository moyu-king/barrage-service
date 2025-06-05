from peewee import CharField, IntegerField
from app.models.base import BaseModel
from app.db import db

class Video(BaseModel):
    name = CharField()
    request_params = CharField()
    platform = IntegerField()


if __name__ == "__main__":
    with db:
        db.create_tables([Video], safe=True)

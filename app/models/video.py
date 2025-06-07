from peewee import CharField, IntegerField, AutoField
from playhouse.sqlite_ext import JSONField
from app.models.base import BaseModel
from app.db import db

class Video(BaseModel):
    id = AutoField()
    name = CharField()
    params = JSONField()
    platform = IntegerField()


if __name__ == "__main__":
    with db:
        db.create_tables([Video], safe=True)

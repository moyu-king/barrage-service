from peewee import SqliteDatabase, Model, CharField, IntegerField
from app.constant import db_path

db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db

class Video(BaseModel):
    name = CharField()
    request_params = CharField()
    platform = IntegerField()


if __name__ == "__main__":
    with db:
        db.create_tables([Video], safe=True)

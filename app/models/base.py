from peewee import Model
from app.db import db

class BaseModel(Model):
    class Meta:
        database = db

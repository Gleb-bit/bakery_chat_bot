import datetime, psycopg2

from peewee import *
from pony.orm import Database, Json, Required
from playhouse.mysql_ext import MySQLConnectorDatabase, JSONField
from settings import DB_CONFIG

db_handle = SqliteDatabase('postgres')


class BaseModel(Model):
    class Meta:
        database = db_handle


class Category(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    # class Meta:
    #     db_table = 'categories'


class Product(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    description = TextField(default=None)
    picture = BlobField()
    category = ForeignKeyField(Category, related_name='bakery', to_field='id', on_delete='cascade',
                               on_update='cascade')
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    # class Meta:
    #     db_table = 'categories'


class UserState(BaseModel):
    """user state inside scenario"""
    user_id = CharField(max_length=100)
    text = TextField()
    step_name = CharField(max_length=10)
    keyboard = TextField()

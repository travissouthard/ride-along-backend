import os
from flask_login import UserMixin
from peewee import *
import datetime
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
    DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this env var for you when you provision the Heroku Postgres Add-on
else:
    DATABASE = SqliteDatabase("content.sqlite")

class Admin(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class Blog(Model):
    title = CharField()
    text = TextField()
    image = CharField() # Actual image
    date = DateField()
    author = CharField()
    trip = CharField()
    # admin info
    last_updated = DateTimeField(default=datetime.datetime.now)
    last_admin = ForeignKeyField(Admin, backref="content")
    
    class Meta:
        database = DATABASE

class Video(Model):
    title = CharField()
    text = TextField()
    url = CharField() # url of posted video for embed
    thumbnail = CharField()
    date = DateField()
    trip = CharField()
    # admin info
    last_updated = DateTimeField(default=datetime.datetime.now)
    last_admin = ForeignKeyField(Admin, backref="content")

    class Meta:
        database = DATABASE

class Product(Model):
    name = CharField()
    description = CharField()
    price = FloatField()
    quantity = IntegerField()
    image = CharField()
    discount = FloatField(default=1)
    trip = CharField()
    # admin info
    last_updated = DateTimeField(default=datetime.datetime.now)
    last_admin = ForeignKeyField(Admin, backref="content")

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Admin, Blog, Video, Product], safe=True)
    print("TABLES created!")
    DATABASE.close()
from peewee import *
import datetime

DATABASE = SqliteDatabase("content.sqlite")

class Admin(Model):
    username = CharField()
    email = CharField()
    password = CharField()

    class Meta:
        database = DATABASE

class Blog(Model):
    title = CharField()
    text = CharField()
    image = BlobField() # Actual image
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
    text = CharField()
    url = CharField() # url of posted video for embed
    thumbnail = BlobField()
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
    image = BlobField()
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
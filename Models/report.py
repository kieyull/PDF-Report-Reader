from peewee import *

db = SqliteDatabase('comms.db')


class Report(Model):
  group_number = CharField(max_length=255)


from peewee import *

db = SqliteDatabase('balances.db')

class BaseModel(Model):
    class Meta:
        database = db
    
class Balance(BaseModel):
    address = CharField()
    balance = CharField()
    updated_block = IntegerField()
    
class Config(BaseModel):
    key = CharField()
    value = CharField()
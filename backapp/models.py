'''from mongoengine import *
from back2c.settings import DBNAME

connect(DBNAME)

class test(Document):
    mid = StringField(max_length=33)
    title = ListField(StringField(max_length=300))
    pub_time = StringField(max_length=50)
    crawl_source = StringField(max_length=100)
    desc = ListField(StringField(max_length=300))
    cat = ListField(StringField(max_length=50))
    img = StringField(max_length=50)
    desc_link = ListField(ListField(StringField(max_length=100)))
    go_link = ListField(ListField(StringField(max_length=100)))'''
# Create your models here.

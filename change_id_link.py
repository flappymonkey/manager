__author__ = 'gaonan'

import pymongo
import hashlib

def change():
    connection = pymongo.Connection('localhost', 27017)
    db = connection['scrapy']
    items = db['ztmhs'].find()
    for item in items:
        desc_id_list=[]
        id_link_list=[]
        for desc_link in item['desc_link']:
            print desc_link[0],desc_link[1]
            url_id = hashlib.md5(desc_link[1]).hexdigest().upper()
            desc_id_list.append([desc_link[0],url_id])
            id_link_list.append([url_id,desc_link[1]])
            db['linkdb'].update({'id':url_id},{'$set':{'id':url_id,'link':desc_link[1]}},upsert=True, safe=True)
        link_url_id = hashlib.md5(item['go_link']).hexdigest().upper()
        db['linkdb'].update({'id':link_url_id},{'$set':{'id':link_url_id,'link':item['go_link']}},upsert=True, safe=True)
        db['ztmhs'].update({'id':item['id']},{'$set':{'desc_link':desc_id_list,'id_link':id_link_list,'go_link_id':link_url_id}},upsert=True, safe=True)

if __name__ == "__main__":
    change()
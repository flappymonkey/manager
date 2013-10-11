#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from back2c.settings import db,db_kill,APP_DIR,SEARCH_HOURS,SPLIT_HOUR
from urllib import unquote
import time
import datetime
import os
import hashlib

import logging
logger = logging.getLogger('backapp')

def parse_list_merge(cur_list):
    cur_str = ''
    if cur_list:
        for item in cur_list:
            cur_str = cur_str + item + ' '
        return cur_str[:-1]
    else:
        return ''
def parse_list_enter(cur_list):
    cur_str = ''
    if cur_list:
        for item in cur_list:
            cur_str = cur_str + item + '\n'
        return cur_str[:-1]
    else:
        return ''
def parse_list_url(cur_list):
    cur_str = ''
    if cur_list:
        for temp_list in cur_list:
            cur_str = cur_str + temp_list[0] + ':' + unquote(temp_list[1]) + '\n'
        return cur_str[:-1]
    else:
        return ''
def split_chinese_return(text):
    if '\r\n' in text:
        return text.split('\r\n')
    else :
        return text.split('\n')
def ret_approve_stat_name(stat):
    if stat == 0:
        return '待发布审核'
    elif stat == 1:
        return '已发布上线'
    elif stat == 2:
        return '待失效审核'
    elif stat == 3:
        return '已删除'
    elif stat == 4:
        return '已发布失效'
    elif stat == 5:
        return '已预发布'
    else:
        return '未知状态'
def ret_index_stat_name(stat,cur_flag):
    if cur_flag == 0:
        if stat == 1:
            return '正常发布'
        elif stat == 4:
            return '失效'
        elif stat == 3:
            return '删除'
        elif stat == 5:
            return '已预发布'
        else:
            return '未知状态'
    elif cur_flag == 1:
        if stat == 1:
            return '置顶'
        else:
            return '非置顶'
    elif cur_flag == 2:
        if stat == 1:
            return '自编辑'
        else:
            return '外网抓取'
    else:
        if stat == 1:
            return '白菜价'
        elif stat == 2:
            return '全网最低'
        else:
            return '其它'

def ret_index_up_name(up):
    if up == 1:
       return '置顶'
    else:
        return '非置顶'
def ret_index_our_cat_name(cat):
    if cat == 1:
        return '白菜价'
    elif cat == 2:
        return '全网最低'
    else:
        return '其它'
def split_desc_link_return(text):
    item_list = []
    desc_id_list = []
    id_link_list = []
    temp_dict = {}
    if '\r\n' in text:
        item_list = text.split('\r\n')
    else :
        item_list = text.split('\n')
    for item in item_list:
        temp_desc_id = []
        temp_id_link = []
        if u'；' in item:
            sp_list = item.split(u'；')
            if len(sp_list) == 2:
                if sp_list[0] in temp_dict:
                    continue
                temp_desc_id.append(sp_list[0])
                temp_desc_id.append(get_link_id(sp_list[1]))
                temp_id_link.append(get_link_id(sp_list[1]))
                temp_id_link.append(sp_list[1])
                desc_id_list.append(temp_desc_id)
                id_link_list.append(temp_id_link)
                temp_dict[sp_list[0]] = 1
        elif ';' in item:
            sp_list = item.split(';')
            if len(sp_list) == 2:
                if sp_list[0] in temp_dict:
                    continue
                temp_desc_id.append(sp_list[0])
                temp_desc_id.append(get_link_id(sp_list[1]))
                temp_id_link.append(get_link_id(sp_list[1]))
                temp_id_link.append(sp_list[1])
                desc_id_list.append(temp_desc_id)
                id_link_list.append(temp_id_link)
                temp_dict[sp_list[0]] = 1
    return desc_id_list,id_link_list
def parse_desc_link_return(cur_list):
    cur_str = ''
    if cur_list:
        for item in cur_list:
            cur_str = cur_str + item[0] + u'；' + unquote(item[1]) + '\n'
        return cur_str[:-1]
    else:
        return ''

def parse_index_desc_link_return(desc_id,id_link):
    cur_str = ''
    if desc_id and id_link and len(desc_id)==len(id_link):
        length = len(desc_id)
        for i in range(0,length):
            cur_str = cur_str + desc_id[i][0] + u'；' + id_link[i][1] + '\n'
        return cur_str[:-1]
    else:
        return ''

def get_cut_date():
    day_diff = (SEARCH_HOURS * 3600) / 86400
    sec_diff = (SEARCH_HOURS * 3600) % 86400
    cur_time_diff = datetime.timedelta(days = day_diff,seconds = sec_diff)
    return (datetime.datetime.now() - cur_time_diff).strftime('%Y-%m-%d %H:%M:%S')

def get_day_start_unix():
    cur_str = datetime.datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
    return int(time.mktime(time.strptime(cur_str,'%Y-%m-%d %H:%M:%S')))
def unix_time_to_str(unix_time):
    value = time.localtime(unix_time)
    return time.strftime('%Y-%m-%d %H:%M:%S', value)
def str_to_unix_time(str,format):
    return int(time.mktime(time.strptime(str,format)))

def get_split_date(index):
    day_diff = (SPLIT_HOUR * 3600 * index) / 86400
    sec_diff = (SPLIT_HOUR * 3600 * index) % 86400
    cur_time_diff = datetime.timedelta(days = day_diff,seconds = sec_diff)
    return (datetime.datetime.now() - cur_time_diff).strftime('%Y-%m-%d %H:%M:%S')

def get_link_id(url):
    url_sign = hashlib.md5(url).hexdigest().upper()
    return url_sign

def up_load_img(request,id):
    file_obj = request.FILES.get('item_img', None)
    if file_obj:
        img_file_list = file_obj.name.split('.')
        if (cmp(img_file_list[-1],'jpg') == 0) or (cmp(img_file_list[-1],'png') == 0):
            image_name = '%s_%s.%s'%(id,datetime.datetime.now().strftime('%Y%m%d%H%M%S'),img_file_list[-1])
            image_path = os.path.normpath(os.path.join(APP_DIR,'backapp/static/upload_images/%s'%image_name))
            print image_path
            destination = open(image_path,'wb+')
            for chunk in file_obj.chunks():
                destination.write(chunk)
            destination.close()
            return '/static/upload_images/%s'%image_name
        else:
            return None
    else:
        return None

def login(request):
    if request.method == 'POST':
        items = db['userdb'].find({'username':request.POST['username']})
        if items.count() >= 1:
            if cmp(request.POST['passwd'],items[0]['passwd']) == 0:
                flag = 1
            else:
                flag = 0
        else:
            flag = 0
        request.session['userflag'] = flag
    else:
        if request.session.get('userflag'):
            flag = request.session['userflag']
        else:
            flag = 0
    print flag
    if flag == 0:
        return render_to_response('login.html', {}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/main/')


def main(request):
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        request.session['userflag'] = 0
        return HttpResponseRedirect('/login/')
    else:
        return render_to_response('main.html', {},context_instance=RequestContext(request))
def index_all(request):
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    if request.method == 'GET':
        return render_to_response('indexall.html', {},context_instance=RequestContext(request))
    else:
        return render_to_response('indexall.html', {},context_instance=RequestContext(request))
def index(request):
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        if 'cur_flag' in request.POST:
            cur_flag = int(request.POST['cur_flag'])
            print 'cur_flag',cur_flag
        else:
            cur_flag = 0
        stat = int(request.POST['stat'])
        if 'is_search' in request.POST:
            is_search = int(request.POST['is_search'])
        else:
            is_search = 0

        if is_search == 0:
            if cur_flag == 0:
                items = db['ztmhs'].find({'stat':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
            elif cur_flag == 1:
                items = db['ztmhs'].find({'up':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
            elif cur_flag == 2:
                items = db['ztmhs'].find({'is_from':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
            else:
                items = db['ztmhs'].find({'our_cat':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        else:
            items = db['ztmhs'].find({'go_link':request.POST['search_url']}).sort("pub_time",-1)
    elif request.method == 'GET':
        if 'cur_flag' in request.GET:
            cur_flag = int(request.GET['cur_flag'])
        else:
            cur_flag = 0
        if 'cur_stat' in request.GET:
            stat = int(request.GET['cur_stat'])
        else:
            stat = 1
        if cur_flag == 0:
            items = db['ztmhs'].find({'stat':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        elif cur_flag == 1:
            items = db['ztmhs'].find({'up':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        elif cur_flag == 2:
            items = db['ztmhs'].find({'is_from':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        else:
            items = db['ztmhs'].find({'our_cat':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
    i = 0
    current_split_date = get_split_date(i)
    next_split_date = get_split_date(i+1)
    temp_list=[]
    temp_t_list=[]
    for item in items:
        temp_dict={}
        temp_dict['id'] = item['id']
        temp_dict['title'] = item['title']
        temp_dict['pub_time'] = item['pub_time']
        temp_dict['cur_stat'] = stat
        temp_dict['cur_flag'] = cur_flag
        temp_dict['stat'] = ret_index_stat_name(stat,cur_flag)
        if cmp(item['pub_time'],next_split_date) < 0:
            i += 1
            temp_list.append([current_split_date,next_split_date,temp_t_list])
            current_split_date = get_split_date(i)
            next_split_date = get_split_date(i+1)
            temp_t_list=[]
        temp_t_list.append(temp_dict)
    temp_list.append([current_split_date,next_split_date,temp_t_list])
    '''temp_list=[]
    for item in items:
        temp_dict = {}
        temp_dict['id'] = item['id']
        temp_dict['title'] = item['title']
        temp_dict['pub_time'] = item['pub_time']
        temp_dict['cur_stat'] = stat
        temp_dict['cur_flag'] = cur_flag
        temp_dict['stat'] = ret_index_stat_name(stat,cur_flag)
        temp_list.append(temp_dict)'''
    return render_to_response('index.html', {'Items': temp_list,'cur_flag':cur_flag,'cur_stat':stat,'cur_stat_name':ret_index_stat_name(stat,cur_flag)},
        context_instance=RequestContext(request))
def create_feed(request):
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    if request.method == 'GET':
        if 'cur_flag' in request.GET:
            cur_flag = int(request.GET['cur_flag'])
        else:
            cur_flag = 0
        if 'cur_stat' in request.GET:
            stat = int(request.GET['cur_stat'])
        else:
            stat = 1
        return render_to_response('create_feed.html',{'cur_flag':cur_flag,'cur_stat':stat}, context_instance=RequestContext(request))
    else:
        if 'cur_flag' in request.POST:
            cur_flag = int(request.POST['cur_flag'])
        else:
            cur_flag = 0
        if 'cur_stat' in request.POST:
            stat = int(request.POST['cur_stat'])
        else:
            stat = 1
        find_result = db['ztmhs'].find({'go_link':request.POST['go_link']})
        if find_result.count() > 0:
            #已经存在直达链接相同的
            id = find_result[0]['id']
           # return render_to_response('index_detail.html',{'id':id,'cur_flag':cur_flag,'cur_stat':stat,'is_same':1}, context_instance=RequestContext(request))
            return HttpResponseRedirect('/index_detail/?id=%s&cur_flag=%d&cur_stat=%d&is_same=1'%(id,cur_flag,stat))
        save_dict={}
        save_dict['id'] = hashlib.md5(request.POST['go_link']).hexdigest().upper()
        save_dict['title'] = request.POST['title']
        save_dict['flush'] = split_chinese_return(request.POST['flush'])
        save_dict['cat'] = split_chinese_return(request.POST['cat'])
        save_dict['our_cat'] = int(request.POST['our_cat'])
        save_dict['go_link'] = request.POST['go_link']
        save_dict['go_link_id'] = get_link_id(request.POST['go_link'])
        save_dict['source'] = request.POST['source']
        save_dict['source_url'] = '真TM划算'
        save_dict['desc'] = split_chinese_return(request.POST['desc'])
        (save_dict['desc_link'],save_dict['id_link']) = split_desc_link_return(request.POST['desc_link'])
        save_dict['worth'] = int(request.POST['worth'])
        save_dict['bad'] = int(request.POST['bad'])
        save_dict['pub_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_dict['stat'] = int(request.POST['stat']) #上线
        if save_dict['stat'] == 5:
            save_dict['pre_pub_time'] = request.POST['preday']
        else:
            save_dict['pre_pub_time'] = 'NONE'
        save_dict['up'] = int(request.POST['up'])
        cur_obj = up_load_img(request,save_dict['id'])
        if cur_obj:
            save_dict['img'] = cur_obj
        #内部来源
        save_dict['is_from'] = 1
        for id_link in save_dict['id_link']:
            db['linkdb'].update({'id':id_link[0]},{'$set':{'id':id_link[0],'link':id_link[1]}},upsert=True, safe=True)
        db['linkdb'].update({'id':save_dict['go_link_id']},{'$set':{'id':save_dict['go_link_id'],'link':save_dict['go_link']}},upsert=True, safe=True)
        db['ztmhs'].update({'id': save_dict['id']}, { '$set': dict(save_dict) },upsert=True, safe=True)

        if cur_flag == 0:
            items = db['ztmhs'].find({'stat':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        elif cur_flag == 1:
            items = db['ztmhs'].find({'up':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        elif cur_flag == 2:
            items = db['ztmhs'].find({'is_from':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        else:
            items = db['ztmhs'].find({'our_cat':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)

        i = 0
        current_split_date = get_split_date(i)
        next_split_date = get_split_date(i+1)
        temp_list=[]
        temp_t_list=[]
        for item in items:
            temp_dict={}
            temp_dict['title'] = parse_list_merge(item['title'])
            temp_dict['pub_time'] = item['pub_time']
            temp_dict['id'] = item['id']
            temp_dict['cur_stat'] = item['stat']
            temp_dict['stat'] = ret_index_stat_name(item['stat'],int(cur_flag))
            if cmp(item['pub_time'],next_split_date) < 0:
                i += 1
                temp_list.append([current_split_date,next_split_date,temp_t_list])
                current_split_date = get_split_date(i)
                next_split_date = get_split_date(i+1)
                temp_t_list=[]
            temp_t_list.append(temp_dict)
        temp_list.append([current_split_date,next_split_date,temp_t_list])
        '''temp_list=[]
        for item in items:
            temp_dict={}
            temp_dict['title'] = parse_list_merge(item['title'])
            temp_dict['pub_time'] = item['pub_time']
            temp_dict['id'] = item['id']
            temp_dict['cur_stat'] = item['stat']
            temp_dict['stat'] = ret_index_stat_name(item['stat'],int(cur_flag))
            temp_list.append(temp_dict)'''
        template = 'index.html'
        params = {'Items': temp_list,'cur_flag':cur_flag,'cur_stat':stat,'cur_stat_name':ret_index_stat_name(stat,cur_flag)}
        return render_to_response(template, params, context_instance=RequestContext(request))

def index_detail(request):
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        id = eval("request." + request.method + "['id']")
        cur_stat = eval("request." + request.method + "['cur_stat']")
        cur_flag = eval("request." + request.method + "['cur_flag']")
        save_dict={}
        save_dict['id'] = id
        save_dict['title'] = request.POST['title']
        save_dict['flush'] = split_chinese_return(request.POST['flush'])
        save_dict['cat'] = split_chinese_return(request.POST['cat'])
        save_dict['our_cat'] = int(request.POST['our_cat'])
        save_dict['go_link'] = request.POST['go_link']
        save_dict['go_link_id'] = get_link_id(request.POST['go_link'])
        save_dict['source'] = request.POST['source']
        save_dict['desc'] = split_chinese_return(request.POST['desc'])
        (save_dict['desc_link'],save_dict['id_link']) = split_desc_link_return(request.POST['desc_link'])
        save_dict['worth'] = int(request.POST['worth'])
        save_dict['bad'] = int(request.POST['bad'])
        #save_dict['pub_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_dict['pub_time'] = request.POST['pubday']
        save_dict['stat'] = int(request.POST['stat']) #上线

        if save_dict['stat'] == 5:
            save_dict['pre_pub_time'] = request.POST['preday']
        else:
            save_dict['pre_pub_time'] = 'NONE'
        if save_dict['stat'] == 1 or save_dict['stat'] == 5:
            save_dict['up'] = int(request.POST['up'])
        else:
            #状态不为发布时，置顶状态均为失效
            save_dict['up'] = 2
        cur_obj = up_load_img(request,id)
        if cur_obj:
            save_dict['img'] = cur_obj

        for id_link in save_dict['id_link']:
            db['linkdb'].update({'id':id_link[0]},{'$set':{'id':id_link[0],'link':id_link[1]}},upsert=True, safe=True)
        db['linkdb'].update({'id':save_dict['go_link_id']},{'$set':{'id':save_dict['go_link_id'],'link':save_dict['go_link']}},upsert=True, safe=True)
        db['ztmhs'].update({'id': save_dict['id']}, { '$set': dict(save_dict) },upsert=True, safe=True)

        if int(cur_flag) == 0:
            items = db['ztmhs'].find({'stat':int(cur_stat),'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        elif int(cur_flag) == 1:
            items = db['ztmhs'].find({'up':int(cur_stat),'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        elif int(cur_flag) == 2:
            items = db['ztmhs'].find({'is_from':int(cur_stat),'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        else:
            items = db['ztmhs'].find({'our_cat':int(cur_stat),'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)

        i = 0
        current_split_date = get_split_date(i)
        next_split_date = get_split_date(i+1)
        temp_list=[]
        temp_t_list=[]
        for item in items:
            temp_dict={}
            temp_dict['title'] = parse_list_merge(item['title'])
            temp_dict['pub_time'] = item['pub_time']
            temp_dict['id'] = item['id']
            temp_dict['cur_stat'] = item['stat']
            temp_dict['stat'] = ret_index_stat_name(item['stat'],int(cur_flag))
            if cmp(item['pub_time'],next_split_date) < 0:
                i += 1
                temp_list.append([current_split_date,next_split_date,temp_t_list])
                current_split_date = get_split_date(i)
                next_split_date = get_split_date(i+1)
                temp_t_list=[]
            temp_t_list.append(temp_dict)
        temp_list.append([current_split_date,next_split_date,temp_t_list])
        '''temp_list=[]
        for item in items:
            temp_dict={}
            temp_dict['title'] = parse_list_merge(item['title'])
            temp_dict['pub_time'] = item['pub_time']
            temp_dict['id'] = item['id']
            temp_dict['cur_stat'] = item['stat']
            temp_dict['stat'] = ret_index_stat_name(item['stat'],int(cur_flag))
            temp_list.append(temp_dict)'''
        template = 'index.html'
        params = {'Items': temp_list,'cur_flag':int(cur_flag),'cur_stat':int(cur_stat),'cur_stat_name':ret_index_stat_name(int(cur_stat),int(cur_flag))}
    elif request.method == 'GET':
        if 'id' not in request.GET or 'cur_stat' not in request.GET or 'cur_flag' not in request.GET:
            return HttpResponseRedirect('/index/')
        id = eval("request." + request.method + "['id']")
        cur_stat = eval("request." + request.method + "['cur_stat']")
        cur_flag = eval("request." + request.method + "['cur_flag']")
        item = db['ztmhs'].find({"id":id})
        if item:
            temp_dict = {}
            temp_dict['id'] = item[0]['id']
            temp_dict['title'] = item[0]['title']
            temp_dict['flush'] = parse_list_enter(item[0]['flush'])
            temp_dict['pub_time'] = item[0]['pub_time']
            temp_dict['desc'] = parse_list_enter(item[0]['desc'])
            temp_dict['desc_link'] = parse_index_desc_link_return(item[0]['desc_link'],item[0]['id_link'])
            temp_dict['cat'] = parse_list_enter(item[0]['cat'])
            temp_dict['source'] = item[0]['source']
            temp_dict['go_link'] = item[0]['go_link']
            temp_dict['worth'] = item[0]['worth']
            temp_dict['bad'] = item[0]['bad']
            temp_dict['source_url'] = item[0]['source_url']
            temp_dict['img']=item[0]['img']
            temp_dict['cur_stat'] = cur_stat
            temp_dict['cur_flag'] = cur_flag
            temp_dict['pre_pub_time'] = item[0]['pre_pub_time']
            temp_dict['pub_time'] = item[0]['pub_time']
            #temp_dict['stat'] = ret_index_stat_name(item[0]['stat'])
            #temp_dict['up'] = ret_index_up_name(item[0]['up'])
            #temp_dict['our_cat'] = ret_index_our_cat_name(item[0]['our_cat'])
            temp_dict['stat'] = item[0]['stat']
            temp_dict['up'] = item[0]['up']
            temp_dict['our_cat'] = item[0]['our_cat']
        template = 'index_detail.html'
        params = {'item':temp_dict}
        logger.info('id:%s'%temp_dict['id'])
        print 'here'
    return render_to_response(template, params, context_instance=RequestContext(request))

def approve(request):
    # Get all posts from DB
    #items = db['smzdm'].find({"stat":0}).sort("pub_time",pymongo.DESCENDING)
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        stat = int(request.POST['stat'])
        items = db['smzdm'].find({'stat':stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
    elif request.method == 'GET':
        if 'cur_stat' in request.GET:
            stat = int(request.GET['cur_stat'])
        else:
            stat = 0
        items = db['smzdm'].find({"stat":stat,'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)

    i = 0
    current_split_date = get_split_date(i)
    next_split_date = get_split_date(i+1)
    temp_list=[]
    temp_t_list=[]
    for item in items:
        temp_dict={}
        temp_dict['title'] = parse_list_merge(item['title'])
        temp_dict['pub_time'] = item['pub_time']
        temp_dict['id'] = item['id']
        temp_dict['stat'] = item['stat']
        temp_dict['cur_stat'] = item['stat']
        if cmp(item['pub_time'],next_split_date) < 0:
            i += 1
            temp_list.append([current_split_date,next_split_date,temp_t_list])
            current_split_date = get_split_date(i)
            next_split_date = get_split_date(i+1)
            temp_t_list=[]
        temp_t_list.append(temp_dict)
    temp_list.append([current_split_date,next_split_date,temp_t_list])
    return render_to_response('approve.html', {'Items': temp_list,'cur_stat':stat,'cur_stat_name':ret_approve_stat_name(stat)},
        context_instance=RequestContext(request))
def approve_detail(request):
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        id = eval("request." + request.method + "['id']")
        cur_stat = eval("request." + request.method + "['cur_stat']")
        set_stat = int(request.POST['stat'])
        if set_stat == 1 or set_stat == 4 or set_stat == 5:
            #发布,失效或者预发布的才会同步到线上状态
            save_dict={}
            save_dict['id'] = id
            save_dict['title'] = request.POST['title']
            save_dict['flush'] = split_chinese_return(request.POST['flush'])
            save_dict['cat'] = split_chinese_return(request.POST['cat'])
            save_dict['our_cat'] = int(request.POST['our_cat'])
            save_dict['go_link'] = request.POST['go_link']
            save_dict['go_link_id'] = get_link_id(request.POST['go_link'])
            save_dict['source'] = request.POST['source']
            save_dict['desc'] = split_chinese_return(request.POST['desc'])
            (save_dict['desc_link'],save_dict['id_link']) = split_desc_link_return(request.POST['desc_link'])
            save_dict['worth'] = int(request.POST['worth'])
            save_dict['bad'] = int(request.POST['bad'])
            save_dict['pub_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_dict['stat'] = set_stat
            save_dict['source_url'] = request.POST['source_url']
            save_dict['up'] = int(request.POST['up'])
            img_obj = up_load_img(request,id)
            save_dict['img'] = up_load_img(request,id)
            if set_stat == 5:
                save_dict['pre_pub_time'] = request.POST['preday']
            else:
                save_dict['pre_pub_time'] = 'NONE'
            #外部来源
            save_dict['is_from'] = 2
            #return 'static/upload_images/%s'%image_name
            db['ztmhs'].update({'id': save_dict['id']}, { '$set': dict(save_dict) },upsert=True, safe=True)
            #修改id_link状态
            for id_link in save_dict['id_link']:
                db['linkdb'].update({'id':id_link[0]},{'$set':{'id':id_link[0],'link':id_link[1]}},upsert=True, safe=True)
            db['linkdb'].update({'id':save_dict['go_link_id']},{'$set':{'id':save_dict['go_link_id'],'link':save_dict['go_link']}},upsert=True, safe=True)
        #修改当前状态
        result = db['smzdm'].update({'id':id}, {'$set':{'stat':int(request.POST['stat'])}},upsert=True, safe=True)
        items = db['smzdm'].find({"stat":int(cur_stat),'pub_time':{"$gte":get_cut_date()}}).sort("pub_time",-1)
        '''temp_list=[]
        for item in items:
            temp_dict={}
            temp_dict['title'] = parse_list_merge(item['title'])
            temp_dict['pub_time'] = item['pub_time']
            temp_dict['id'] = item['id']
            temp_dict['cur_stat'] = item['stat']
            temp_list.append(temp_dict)'''
        i = 0
        current_split_date = get_split_date(i)
        next_split_date = get_split_date(i+1)
        temp_list=[]
        temp_t_list=[]
        for item in items:
            temp_dict={}
            temp_dict['title'] = parse_list_merge(item['title'])
            temp_dict['pub_time'] = item['pub_time']
            temp_dict['id'] = item['id']
            temp_dict['stat'] = item['stat']
            temp_dict['cur_stat'] = item['stat']
            if cmp(item['pub_time'],next_split_date) < 0:
                i += 1
                temp_list.append([current_split_date,next_split_date,temp_t_list])
                current_split_date = get_split_date(i)
                next_split_date = get_split_date(i+1)
                temp_t_list=[]
            temp_t_list.append(temp_dict)
        temp_list.append([current_split_date,next_split_date,temp_t_list])
        template = 'approve.html'
        params = {'Items': temp_list,'cur_stat':int(cur_stat),'cur_stat_name':ret_approve_stat_name(int(cur_stat))}

    elif request.method == 'GET':
        if 'id' not in request.GET or 'cur_stat' not in request.GET:
            return HttpResponseRedirect('/approve/')
        id = eval("request." + request.method + "['id']")
        cur_stat = eval("request." + request.method + "['cur_stat']")
        item = db['smzdm'].find({"id":id})
        if item:
            temp_dict = {}
            temp_dict['id'] = item[0]['id']
            temp_dict['title'] = parse_list_merge(item[0]['title'])
            temp_dict['pub_time'] = item[0]['pub_time']
            temp_dict['desc'] = parse_list_enter(item[0]['desc'])
            temp_dict['cat'] = parse_list_enter(item[0]['cat'])
            temp_dict['source'] = parse_list_enter(item[0]['source'])
            temp_dict['desc_link'] = parse_desc_link_return(item[0]['desc_link_list'])
            temp_dict['cur_stat'] = item[0]['stat']
            temp_dict['desc_link_show'] = []

            for desc_link in item[0]['desc_link_list']:
                temp_dict['desc_link_show'].append({'desc':desc_link[0],'link':unquote(desc_link[1])})
            temp_dict['go_link'] = []
            for go_link in item[0]['go_link']:
                temp_dict['go_link'].append(unquote(go_link[1]))
            temp_dict['img'] = item[0]['img']
            temp_dict['worth'] = item[0]['worth_num']
            temp_dict['bad'] = item[0]['bad_num']
            temp_dict['crawl_source'] = item[0]['crawl_source']
            temp_dict['source_url'] = item[0]['source_url']

            temp_dict['same_source_url']=''
            temp_dict['same_stat']=''
            if cmp(item[0]['same_id'],'NONE') != 0:
                #存在相同id
                same_item = db['smzdm'].find({"id":item[0]['same_id']})
                if same_item:
                    temp_dict['same_source_url'] = same_item[0]['source_url']
                    if same_item[0]['stat'] == 0:
                        temp_dict['same_stat'] = '待审核'
                    elif same_item[0]['stat'] == 1:
                        temp_dict['same_stat'] = '已发布'
                    else:
                        temp_dict['same_stat'] = '已失效'
            #print temp_dict['img'],item[0]['img']
        template = 'approve_detail.html'
        params = {'item':temp_dict}
    return render_to_response(template, params, context_instance=RequestContext(request))

def seckill(request):
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    begin_time = get_day_start_unix()
    end_time = begin_time + 86400
    current_time = int(time.time())
    if request.method == 'POST':
        if 'sort_flag' in request.POST:
            sort_flag = int(request.POST['sort_flag'])
        else:
            sort_flag = 1
        if 'stat' in request.POST:
            stat = int(request.POST['stat'])
        else:
            stat = 2
        if 'is_search' in request.POST:
            is_search = int(request.POST['is_search'])
        else:
            is_search = 0
        if is_search == 0:
            if stat == 1:
                cursor = db_kill['seckill'].find({'stat':stat,'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gt":current_time,"$lte":end_time}})
            elif stat == 2:
                cursor = db_kill['seckill'].find({'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gte":begin_time,"$lte":current_time},'stat':{'$in':[1,stat]}})
            elif stat == 3:
                cursor = db_kill['seckill'].find({'stat':{'$in':[1,2,stat]},'display_time_begin':{"$gte":begin_time},'display_time_end':{"$gt":begin_time,"$lt":current_time}})
            else:
                cursor = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":begin_time}})
            if sort_flag == 1:
                #按价格
                items = cursor.sort('cur_price',1)
                #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('cur_price',1)
            elif sort_flag == 2:
                #按销量
                items = cursor.sort('sale_percent',-1)
                #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('sale_percent',-1)
            else:
                #按开始时间
                items = cursor.sort('display_time_begin',-1)
                #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('display_time_begin',-1)
        else:
            items = db_kill['seckill'].find({'display_time_begin':{"$gte":get_day_start_unix()},'$or':[{'link':{"$regex":request.POST['search_url']}},{'title':{"$regex":request.POST['search_url']}}]})
        final_list = []
        result_list = []
        top_list = []
        for item in items:
            temp_dict={}
            temp_dict['id'] = item['id']
            temp_dict['title'] = item['title']
            #temp_dict['img'] = item['img']
            if 'cur_price' in item and item['cur_price'] >= 0:
                temp_dict['cur_price'] = '%.2f 元'%(float(item['cur_price']) / 100)
            else:
                temp_dict['cur_price'] = '未知'
            if 'ori_price' in item and item['ori_price'] >= 0:
                temp_dict['ori_price'] = '%.2f 元'%(float(item['ori_price']) / 100)
            else:
                temp_dict['ori_price'] = '未知'
            if 'discount' in item and item['discount'] > 0:
                temp_dict['discount'] = '%.1f 折'%(float(item['discount']) / 10)
            else:
                temp_dict['discount'] = '未知'
            temp_dict['limit'] = item['limit']
            if 'sale_percent' in item:
                temp_dict['sale_percent'] = item['sale_percent']
            else:
                temp_dict['sale_percent'] = -1
                #temp_dict['link'] = item['link']
            temp_dict['source'] = item['source']
            if 'display_time_begin' in item:
                temp_dict['time_begin'] = unix_time_to_str(item['display_time_begin'])
            else:
                temp_dict['time_begin'] = '无'
            if 'display_time_end' in item:
                temp_dict['time_end'] = unix_time_to_str(item['display_time_end'])
            else:
                temp_dict['time_end'] = '无'
            if 'up' in item and item['up'] == 1:
                top_list.append(temp_dict)
            else:
                result_list.append(temp_dict)
        final_list.append(['置顶结果',top_list])
        final_list.append(['非置顶结果',result_list])
    elif request.method == 'GET':
        if 'sort_flag' in request.GET:
            sort_flag = int(request.GET['sort_flag'])
        else:
            sort_flag = 1
        if 'cur_stat' in request.GET:
            stat = int(request.GET['cur_stat'])
        else:
            stat = 2
        if stat == 1:
            cursor = db_kill['seckill'].find({'stat':stat,'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gt":current_time,"$lte":end_time}})
        elif stat == 2:
            cursor = db_kill['seckill'].find({'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gte":begin_time,"$lte":current_time},'stat':{'$in':[1,stat]}})
        elif stat == 3:
            cursor = db_kill['seckill'].find({'stat':{'$in':[1,2,stat]},'display_time_begin':{"$gte":begin_time},'display_time_end':{"$gt":begin_time,"$lt":current_time}})
        else:
            cursor = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":begin_time}})
        if sort_flag == 1:
            #按价格
            items = cursor.sort('cur_price',1)
            #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('cur_price',1)
        elif sort_flag == 2:
            #按销量
            items = cursor.sort('sale_percent',-1)
            #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('sale_percent',-1)
        else:
            #按开始时间
            items = cursor.sort('display_time_begin',-1)
            #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('display_time_begin',-1)
        result_list = []
        top_list = []
        final_list = []
        for item in items:
            temp_dict={}
            temp_dict['id'] = item['id']
            temp_dict['title'] = item['title']
            #temp_dict['img'] = item['img']
            if 'cur_price' in item and item['cur_price'] >= 0:
                temp_dict['cur_price'] = '%.2f 元'%(float(item['cur_price']) / 100)
            else:
                temp_dict['cur_price'] = '未知'
            if 'ori_price' in item and item['ori_price'] >= 0:
                temp_dict['ori_price'] = '%.2f 元'%(float(item['ori_price']) / 100)
            else:
                temp_dict['ori_price'] = '未知'
            if 'discount' in item and item['discount'] > 0:
                temp_dict['discount'] = '%.1f 折'%(float(item['discount']) / 10)
            else:
                temp_dict['discount'] = '未知'
            temp_dict['limit'] = item['limit']
            if 'sale_percent' in item:
                temp_dict['sale_percent'] = item['sale_percent']
            else:
                temp_dict['sale_percent'] = -1
            #temp_dict['link'] = item['link']
            temp_dict['source'] = item['source']
            if 'display_time_begin' in item:
                temp_dict['time_begin'] = unix_time_to_str(item['display_time_begin'])
            else:
                temp_dict['time_begin'] = '无'
            if 'display_time_end' in item:
                temp_dict['time_end'] = unix_time_to_str(item['display_time_end'])
            else:
                temp_dict['time_end'] = '无'
            if 'up' in item and item['up'] == 1:
                top_list.append(temp_dict)
            else:
                result_list.append(temp_dict)
        final_list.append(['置顶结果',top_list])
        final_list.append(['非置顶结果',result_list])
    return render_to_response('seckill.html', {'Items': final_list,'sort_flag':sort_flag,'cur_stat':stat},context_instance=RequestContext(request))

def seckill_detail(request):
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    begin_time = get_day_start_unix()
    end_time = begin_time + 86400
    current_time = int(time.time())
    if request.method == 'POST':
        id = eval("request." + request.method + "['id']")
        stat = int(eval("request." + request.method + "['cur_stat']"))
        sort_flag = int(eval("request." + request.method + "['sort_flag']"))
        save_dict={}
        save_dict['title'] = request.POST['title']
        save_dict['link'] = request.POST['link']
        save_dict['sale_percent'] = int(request.POST['sale_percent'])
        if save_dict['sale_percent'] > 100:
            save_dict['sale_percent'] = 100
        cur_obj = up_load_img(request,id)
        if cur_obj:
            save_dict['img'] = cur_obj
        save_dict['stat'] = int(request.POST['stat'])
        save_dict['up'] = int(request.POST['up'])
        db_kill['seckill'].update({'id':id}, { '$set': dict(save_dict) },upsert=True, safe=True)
        if stat == 1:
            cursor = db_kill['seckill'].find({'stat':stat,'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gt":current_time,"$lte":end_time}})
        elif stat == 2:
            cursor = db_kill['seckill'].find({'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gte":begin_time,"$lte":current_time},'stat':{'$in':[1,stat]}})
        elif stat == 3:
            cursor = db_kill['seckill'].find({'stat':{'$in':[1,2,stat]},'display_time_begin':{"$gte":begin_time},'display_time_end':{"$gt":begin_time,"$lt":current_time}})
        else:
            cursor = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":begin_time}})
        if sort_flag == 1:
            #按价格
            items = cursor.sort('cur_price',1)
            #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('cur_price',1)
        elif sort_flag == 2:
            #按销量
            items = cursor.sort('sale_percent',-1)
            #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('sale_percent',-1)
        else:
            #按开始时间
            items = cursor.sort('display_time_begin',-1)
        result_list = []
        top_list = []
        final_list = []
        for item in items:
            temp_dict={}
            temp_dict['id'] = item['id']
            temp_dict['title'] = item['title']
            #temp_dict['img'] = item['img']
            if 'cur_price' in item and item['cur_price'] >= 0:
                temp_dict['cur_price'] = '%.2f 元'%(float(item['cur_price']) / 100)
            else:
                temp_dict['cur_price'] = '未知'
            if 'ori_price' in item and item['ori_price'] >= 0:
                temp_dict['ori_price'] = '%.2f 元'%(float(item['ori_price']) / 100)
            else:
                temp_dict['ori_price'] = '未知'
            if 'discount' in item and item['discount'] > 0:
                temp_dict['discount'] = '%.1f 折'%(float(item['discount']) / 10)
            else:
                temp_dict['discount'] = '未知'
            temp_dict['limit'] = item['limit']
            if 'sale_percent' in item:
                temp_dict['sale_percent'] = item['sale_percent']
            else:
                temp_dict['sale_percent'] = -1
                #temp_dict['link'] = item['link']
            temp_dict['source'] = item['source']
            if 'display_time_begin' in item:
                temp_dict['time_begin'] = unix_time_to_str(item['display_time_begin'])
            else:
                temp_dict['time_begin'] = '无'
            if 'display_time_end' in item:
                temp_dict['time_end'] = unix_time_to_str(item['display_time_end'])
            else:
                temp_dict['time_end'] = '无'
            if 'up' in item and item['up'] == 1:
                top_list.append(temp_dict)
            else:
                result_list.append(temp_dict)
        final_list.append(['置顶结果',top_list])
        final_list.append(['非置顶结果',result_list])
        template = 'seckill.html'
        params = {'Items': final_list,'sort_flag':sort_flag,'cur_stat':stat}
    elif request.method == 'GET':
        if 'id' not in request.GET or 'cur_stat' not in request.GET or 'sort_flag' not in request.GET:
            return HttpResponseRedirect('/seckill/')
        id = eval("request." + request.method + "['id']")
        cur_stat = eval("request." + request.method + "['cur_stat']")
        sort_flag = eval("request." + request.method + "['sort_flag']")
        item = db_kill['seckill'].find_one({"id":id})
        temp_dict={}
        if item:
            temp_dict['id'] = item['id']
            temp_dict['title'] = item['title']
            temp_dict['img'] = item['img']
            temp_dict['link'] = item['link']
            if 'cur_price' in item and item['cur_price'] >= 0:
                temp_dict['cur_price'] = '%.2f 元'%(float(item['cur_price']) / 100)
            else:
                temp_dict['cur_price'] = '未知'
            if 'ori_price' in item and item['ori_price'] >= 0:
                temp_dict['ori_price'] = '%.2f 元'%(float(item['ori_price']) / 100)
            else:
                temp_dict['ori_price'] = '未知'
            if 'discount' in item and item['discount'] > 0:
                temp_dict['discount'] = '%.1f 折'%(float(item['discount']) / 10)
            else:
                temp_dict['discount'] = '未知'
            temp_dict['limit'] = item['limit']
            if 'sale_percent' in item:
                temp_dict['sale_percent'] = item['sale_percent']
            else:
                temp_dict['sale_percent'] = -1
                temp_dict['link'] = item['link']
            temp_dict['source'] = item['source']
            if 'display_time_begin' in item:
                temp_dict['time_begin'] = unix_time_to_str(item['display_time_begin'])
            else:
                temp_dict['time_begin'] = '无'
            if 'display_time_end' in item:
                temp_dict['time_end'] = unix_time_to_str(item['display_time_end'])
            else:
                temp_dict['time_end'] = '无'
            if 'up' in item:
                temp_dict['up'] = item['up']
            else:
                temp_dict['up'] = 2
            temp_dict['stat'] = int(cur_stat)
            temp_dict['sort_flag'] = int(sort_flag)
            template = 'seckill_detail.html'
        params = {'item':temp_dict}
    return render_to_response(template, params, context_instance=RequestContext(request))
def create_seckill(request):
    if (not request.session.get('userflag')) or request.session['userflag'] != 1:
        return HttpResponseRedirect('/login/')
    begin_time = get_day_start_unix()
    end_time = begin_time + 86400
    current_time = int(time.time())
    if request.method == 'POST':
        if 'sort_flag' in request.POST:
            sort_flag = int(request.POST['sort_flag'])
        else:
            sort_flag = 1
        if 'cur_stat' in request.POST:
            stat = int(request.POST['cur_stat'])
        else:
            stat = 2
        save_dict = {}
        save_dict['title'] = request.POST['title']
        save_dict['link'] = request.POST['link']
        save_dict['source'] = request.POST['source']
        save_dict['id'] = hashlib.md5(request.POST['link']).hexdigest().upper()
        save_dict['cur_price'] = int(float(filter(lambda ch:ch in '0123456789.', request.POST['cur_price']))*100)
        save_dict['discount'] = int(float(filter(lambda ch:ch in '0123456789.', request.POST['discount']))*10)
        if float(save_dict['discount']) > 10:
            save_dict['discount'] = 10
        save_dict['ori_price'] = int(save_dict['cur_price'] * 100 / float(save_dict['discount']))
        save_dict['limit'] = int(filter(lambda ch:ch in '-0123456789', request.POST['limit']))
        save_dict['sale_percent'] = int(filter(lambda ch:ch in '-0123456789', request.POST['sale_percent']))
        if save_dict['sale_percent'] > 100:
            save_dict['sale_percent'] = 100
        elif save_dict['sale_percent'] < 0:
            save_dict['sale_percent'] = -1
        cur_obj = up_load_img(request,save_dict['id'])
        if cur_obj:
            save_dict['img'] = cur_obj
        save_dict['stat'] = int(request.POST['stat'])
        save_dict['up'] = int(request.POST['up'])
        if cmp(request.POST['time_begin'],'0') != 0:
            save_dict['actual_time_begin'] = str_to_unix_time(request.POST['time_begin'],'%Y-%m-%d %H:%M')
            save_dict['display_time_begin'] = save_dict['actual_time_begin']
        if cmp(request.POST['time_end'],'0') != 0:
            save_dict['actual_time_end'] = str_to_unix_time(request.POST['time_end'],'%Y-%m-%d %H:%M')
            save_dict['display_time_end'] = save_dict['actual_time_end']

        db_kill['seckill'].update({'id':save_dict['id']}, { '$set': dict(save_dict) },upsert=True, safe=True)
        if stat == 1:
            cursor = db_kill['seckill'].find({'stat':stat,'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gt":current_time,"$lte":end_time}})
        elif stat == 2:
            cursor = db_kill['seckill'].find({'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gte":begin_time,"$lte":current_time},'stat':{'$in':[1,stat]}})
        elif stat == 3:
            cursor = db_kill['seckill'].find({'stat':{'$in':[1,2,stat]},'display_time_begin':{"$gte":begin_time},'display_time_end':{"$gt":begin_time,"$lt":current_time}})
        else:
            cursor = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":begin_time}})
        if sort_flag == 1:
            #按价格
            items = cursor.sort('cur_price',1)
            #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('cur_price',1)
        elif sort_flag == 2:
            #按销量
            items = cursor.sort('sale_percent',-1)
            #items = db_kill['seckill'].find({'stat':stat,'display_time_begin':{"$gte":get_day_start_unix()}}).sort('sale_percent',-1)
        else:
            #按开始时间
            items = cursor.sort('display_time_begin',-1)
        result_list = []
        top_list = []
        final_list = []
        for item in items:
            temp_dict={}
            temp_dict['id'] = item['id']
            temp_dict['title'] = item['title']
            #temp_dict['img'] = item['img']
            if 'cur_price' in item and item['cur_price'] >= 0:
                temp_dict['cur_price'] = '%.2f 元'%(float(item['cur_price']) / 100)
            else:
                temp_dict['cur_price'] = '未知'
            if 'ori_price' in item and item['ori_price'] >= 0:
                temp_dict['ori_price'] = '%.2f 元'%(float(item['ori_price']) / 100)
            else:
                temp_dict['ori_price'] = '未知'
            if 'discount' in item and item['discount'] > 0:
                temp_dict['discount'] = '%.1f 折'%(float(item['discount']) / 10)
            else:
                temp_dict['discount'] = '未知'
            temp_dict['limit'] = item['limit']
            if 'sale_percent' in item:
                temp_dict['sale_percent'] = item['sale_percent']
            else:
                temp_dict['sale_percent'] = -1
                #temp_dict['link'] = item['link']
            temp_dict['source'] = item['source']
            if 'display_time_begin' in item:
                temp_dict['time_begin'] = unix_time_to_str(item['display_time_begin'])
            else:
                temp_dict['time_begin'] = '无'
            if 'display_time_end' in item:
                temp_dict['time_end'] = unix_time_to_str(item['display_time_end'])
            else:
                temp_dict['time_end'] = '无'
            if 'up' in item and item['up'] == 1:
                top_list.append(temp_dict)
            else:
                result_list.append(temp_dict)
        final_list.append(['置顶结果',top_list])
        final_list.append(['非置顶结果',result_list])
        return render_to_response('seckill.html', {'Items': final_list,'sort_flag':sort_flag,'cur_stat':stat},context_instance=RequestContext(request))
    elif request.method == 'GET':
        if 'sort_flag' in request.GET:
            sort_flag = int(request.GET['sort_flag'])
        else:
            sort_flag = 1
        if 'cur_stat' in request.GET:
            stat = int(request.GET['cur_stat'])
        else:
            stat = 2
        return render_to_response('create_seckill.html',{'sort_flag':sort_flag,'cur_stat':stat}, context_instance=RequestContext(request))


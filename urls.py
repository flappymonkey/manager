from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'back2c.backapp.views.login'),
    url(r'^login/', 'back2c.backapp.views.login'),
    url(r'^main/', 'back2c.backapp.views.main'),
    url(r'^indexall/', 'back2c.backapp.views.index_all'),
    url(r'^approve/', 'back2c.backapp.views.approve'),
    url(r'^approve_detail/', 'back2c.backapp.views.approve_detail'),
    url(r'^index/', 'back2c.backapp.views.index'),
    url(r'^create_feed/', 'back2c.backapp.views.create_feed'),
    url(r'^index_detail/', 'back2c.backapp.views.index_detail'),
    url(r'^seckill/', 'back2c.backapp.views.seckill'),
    url(r'^seckill_detail/', 'back2c.backapp.views.seckill_detail'),
    url(r'^create_seckill/', 'back2c.backapp.views.create_seckill'),
)

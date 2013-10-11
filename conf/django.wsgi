import os
import sys
sys.path.append('/home/ops/ToC')
sys.path.append('/home/ops/ToC/back2c')
sys.path.append('/home/ops/ToC/back2c/backapp')
os.environ['DJANGO_SETTINGS_MODULE'] = 'back2c.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

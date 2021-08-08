# -*- coding: utf-8 -*-
from __future__ import absolute_import

# import gevent.monkey
from diveclass.settings import CONFIG


# gevent.monkey.patch_all()

bind = '0.0.0.0:{}'.format(CONFIG['SERVER_PORT'])
workers = CONFIG['GUNICORN_WORKER_NUM']
# worker_class = 'gevent'

proc_name = 'gunicorn-pubhub'

errorlog = '-'
accesslog = '-'

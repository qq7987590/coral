# -*- coding:utf-8 -*-
from psycopg2 import pool
from ...settings import CONFIG
from contextlib import contextmanager

pg_config = CONFIG['postgres']
# pg = psycopg2.connect(
#    database=pg_config['database'], user=pg_config['user'],
#    password=pg_config['password'],
#    host=pg_config['host'], port=pg_config['port'])
pool = pool.ThreadedConnectionPool(1, 3,
                              database=pg_config['database'],
                              user=pg_config['user'],
                              password=pg_config['password'],
                              host=pg_config['host'],
                              port=pg_config['port'])


@contextmanager
def get_pg_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)

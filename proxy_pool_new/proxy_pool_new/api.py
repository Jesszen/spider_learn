from flask import Flask,g
from .db import RedisClient

__all__ =['app']

app = Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):
        g.redis=RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h2> welcome to proxy pool sysytem</h2>'

@app.route('/random')
def get_proxy():
    """
    随机获取代理
    :return: 随机代理
    """
    conn=get_conn()
    return conn.random()

@app.route('/count')
def get_count():
    """
    代理池代理总数
    :return:
    """
    conn=get_conn()
    return str(conn.count())

if __name__=='__main__':
    app.run()
    
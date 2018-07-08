# redis 数据库地址，腾讯云的ip地址
REDIS_HOST = '118.24.26.227'

#端口
REDIS_PORT = 6379

#密码
REDIS_PASSWORD = '123456!'

REDIS_KEY = 'proxies_2'

#代理分数
MAX_SCRORE = 100
MIN_SCORE = 0

#初始分数
INITIAL_SCORE = 10


#代理池数量上限
POOL_UPPER_THRESHOLD = 1000

#测试url，测试代理是否可用
Test_url='http://www.baidu.com'


#最大批次测似数量
Batch_test_size = 100

#检查周期
Tester_cycle = 20

#获取周期
Getter_cycle = 20

#开关
Tester_enabled = True
Getter_enabled = True
Api_enabled = True

#api配置
Api_host='0.0.0.0'
Api_port=5555


VALID_STATUS_CODES = [200, 302]





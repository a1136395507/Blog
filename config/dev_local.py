import pymysql
from dbutils.pooled_db import PooledDB


class DBINFO_MYSQL:
    server = "127.0.0.1"
    password = "ZwLcYfk3AALPkLGE"
    db = "sm_stat"
    user = "sm_stat"
    port = 3306


class DBINFO_REDIS:
    pass


class DB_USER_INFO_MYSQL:
    PYMYSQL_POOL = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=15,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=0,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=6,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=0,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=1,
        # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host='1277.0.0.1',
        port=3306,
        user='sm_insight',
        password='ZwLcINsightk3AALPkLGE',
        database='sm_webapp_sl',  # 链接的数据库的名字
        charset='utf8'
    )


class DB_BLOG_PRODUCT_MYSQL:
    PYMYSQL_POOL = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=15,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=0,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=6,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=0,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=1,
        # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host='172.16.6.247',
        port=3306,
        user='sm_insight',
        password='ZwLcINsightk3AALPkLGE',
        database='sm_product',  # 链接的数据库的名字
        charset='utf8'
    )


DB_URL = "mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db}?charset=utf8".format(
    db_user=DBINFO_MYSQL.user,
    db_password=DBINFO_MYSQL.password,
    db_host=DBINFO_MYSQL.server,
    db_port=DBINFO_MYSQL.port,
    db=DBINFO_MYSQL.db)

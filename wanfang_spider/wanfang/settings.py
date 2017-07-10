# -*- coding: utf-8 -*-

# Scrapy settings for wanfang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import pymysql

BOT_NAME = 'wanfang'

SPIDER_MODULES = ['wanfang.spiders']
NEWSPIDER_MODULE = 'wanfang.spiders'
ITEM_PIPELINES = {
   'wanfang.pipelines.WanfangPipeline': 300,
}

################数据库操作##################
serverIP = '1.1.1.1'
sqluser = 'xx'
sqlpsw = 'xxx'
sqldatabase = 'wanfang'
db = pymysql.connect(serverIP, sqluser, sqlpsw, sqldatabase)
cursor = db.cursor()
#建表如果不存在
sqlcreatetable = """create TABLE if not EXISTS wanfang (
url varchar(500) not null PRIMARY KEY ,
title text not NULL ,
click varchar(100) ,
down varchar(100) ,
des text,
zuozhe text,
kanming text,
yingwenkanming text,
keyword text,
lanmuname text,
doi text,
cankao text,
yinzheng text,
sswenxian text,
sswaiwen text,
sshuiyi text,
ssxuewei text
)DEFAULT CHARSET=utf8
"""
cursor.execute(sqlcreatetable)
cursor.execute("SET NAMES utf8")
cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
# 设置连接等待时间
cursor.execute( "set interactive_timeout=24*3600")

db.commit()

################ip池操作##################
# PROXIES = list()
# with open('mt_proxy.txt', 'r') as filer:
#    content = filer.readlines()
#    for line in content[2:]:
#       PROXIES.append(line.strip())



# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'wanfang.middlewares.ProxyMiddleware':100,
   # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
   # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   # 'wanfang.middlewares.MyCustomDownloaderMiddleware': 543,
   'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
   'wanfang.HttpProxyMiddleware.HttpProxyMiddleware': 543,
}
DOWNLOAD_TIMEOUT = 10

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wanfang (+http://www.yourdomain.com)'



# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32


# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16



# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'wanfang.middlewares.MyCustomSpiderMiddleware': 543,
#}



# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'wanfang.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

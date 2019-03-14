# -*- coding: utf-8 -*-

# Scrapy settings for FaxinSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'FaxinSpider'

SPIDER_MODULES = ['FaxinSpider.spiders']
NEWSPIDER_MODULE = 'FaxinSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'FaxinSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# LOG_LEVEL = 'WARNING'

COOKIE = {'isAutoLogin': 'off', 'ASP.NET_SessionId': 'i2pjidhmtyu4aupiv0vk3w24', 'Hm_lvt_a317640b4aeca83b20c90d410335b70f': '1552267033,1552353636,1552370693', 'Hm_lvt_a4967c0c3b39fcfba3a7e03f2e807c06': '1552302923,1552353636,1552370694', 'sid': 'i2pjidhmtyu4aupiv0vk3w24', 'lawapp_web': '1C39241FF3B0864EC82E5009D4896E20253540AE1EFF5660F223CFADE54E9C41A2CF76EADB39F318257865C28FB028B3390449554A6A18B2A0E6CB99EC608523B7460EF4C42472107E89F21A8945A1BCDADA6E2AB9D5BA34518C208A4AA52016C892028E8DF328396A4EF3F1196D8C401E8AC80408D82F2699D08D10EB98F87B327668951FD28C8A45C03DCB004DD894DF1E45C0424B4113A121B2A6317AD17F99A90920', 'Hm_lpvt_a4967c0c3b39fcfba3a7e03f2e807c06': '1552376125', 'Hm_lpvt_a317640b4aeca83b20c90d410335b70f': '1552376534'}

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'FaxinSpider.middlewares.FaxinspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'FaxinSpider.middlewares.FaxinspiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'FaxinSpider.pipelines.FaxinspiderPipeline': 300,
   'scrapy_redis.pipelines.RedisPipeline': 300,
}

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

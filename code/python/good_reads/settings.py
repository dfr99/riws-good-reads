# -*- coding: utf-8 -*-

# Scrapy settings for good_reads project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
# https://docs.scrapy.org/en/latest/topics/settings.html

BOT_NAME = "good_reads"
SPIDER_MODULES = ["good_reads.spiders"]
NEWSPIDER_MODULE = "good_reads.spiders"

ITEM_PIPELINES = {
    "pipelines.GoodReadsPipeline": 300
}

# DOWNLOADER_MIDDLEWARES = {
#     "middlewares.RotateUserAgentMiddleware": 543,
# }

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Settings to control the scraping process
COOKIES_ENABLE = False

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5.0
AUTOTHROTTLE_MAX_DELAY = 60.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
DOWNLOAD_DELAY = 2.0
CONCURRENT_REQUESTS_PER_DOMAIN = 10
CLOSESPIDER_ITEMCOUNT = 1000

USER_AGENT_CYCLING_INTERVAL = 5
USER_AGENT_LIST = [
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (1)',
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (2)',
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (3)',
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (4)',
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (5)',
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (6)',
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (7)',
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (8)',
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (9)',
    'RIWS-MUEI-FIC-UDC Scrapy Bot - Course Assigment (10)'
]

TELNETCONSOLE_ENABLED = False

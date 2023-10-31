"""
Define your execution for crawling here
"""

# -*- coding: utf-8 -*-
from scrapy.cmdline import execute

try:
    execute (
        [
            "scrapy",
            "crawl",
            "good_reads"
        ]
    )
except SystemExit:
    pass

# -*- coding: utf-8 -*-
#
# Define your execution for crawling here
#

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

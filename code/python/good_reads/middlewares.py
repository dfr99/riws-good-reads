# -*- coding: utf-8 -*-

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent_list, user_agent_cycling_interval):
        super().__init__()
        self.user_agent_list = user_agent_list
        self.user_agent_cycling_interval = user_agent_cycling_interval

    def process_request(self, request, spider):
        if hasattr(spider, 'user_agent_index'):
            spider.user_agent_index += 1
        else:
            spider.user_agent_index = 0

        if spider.user_agent_index % self.user_agent_cycling_interval == 0:
            user_agent = random.choice(self.user_agent_list)
            request.headers['User-Agent'] = user_agent

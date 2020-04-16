# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.utils.project import get_project_settings
from fake_useragent import UserAgent
from spider.comm.proxies import Proxies
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import random
import sys
sys.setrecursionlimit(5000)


class UADownloaderMiddleware(object):
    key_name = 'UserAgent'
    ua_list = []

    def __init__(self):
        # redis = RedisUtil()
        # self.client = redis.get_client()

        # length = self.client.llen(self.key_name)
        # if length == 0:
            try:
                ua = UserAgent().data['browsers'].values()
                for u in ua:
                    self.ua_list.extend(u)
                for u in self.ua_list:
                    self.client.lpush(self.key_name, u)
            except Exception as e:
                print(e)

        # self.ua_list = self.client.lrange(self.key_name, 0, length)
        # redis.close_client()

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.ua_list)



class SpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    settings = get_project_settings()
    is_random_ua = settings.get('IS_RANDOM_UA')
    is_random_proxy = settings.get('IS_RANDOM_PROXY')

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if self.is_random_ua == 1:
                u = UserAgent().random
        else:
                u = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
                    ' (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        request.headers['User-Agent'] = u

        if self.is_random_proxy == 1:
            proxy = Proxies().getProxy()
            request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RetryRecordMiddleware(RetryMiddleware):

    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)

    def process_exception(self, request, exception, spider):
        to_return = RetryMiddleware.process_exception(
            self, request, exception, spider)
        # customize retry middleware by modifying this
        request.meta['url'] = request.url
        self.record_failed('failed.txt', request, exception, 'url')
        return to_return

    def record_failed(self, path, request, exception, failed_meta):
        failed_list = request.meta.get(failed_meta, [])
        failed_list = [x.strip() for x in failed_list]
        of = open(path, 'a')
        of.write('%s\n' % ''.join(failed_list))
        of.close()


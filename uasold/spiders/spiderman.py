# -*- coding: utf-8 -*-
"""Simple scrapper based on generic CrawlSpider to grasp all pages from website
and download static files"""
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


def counter():
    a = 1
    while True:
        yield a
        a += 1


class SpiderMan(CrawlSpider):
    name = "auditua"
    allowed_domains = ['auditua.com.ua']
    start_urls = [
        'http://auditua.com.ua/',
    ]

    rules = (
        Rule(LinkExtractor(allow=(), deny=('print=1',)), callback='parse_static', follow=True),
    )

    int_gen = counter()

    def parse_static(self, response):
        self.logger.info('='*30)
        for href in response.css('link::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.save_file)
        for src in response.css('script::attr(src)').extract():
            yield scrapy.Request(response.urljoin(src), callback=self.save_file)
        for src in response.css('img::attr(src)').extract():
            yield scrapy.Request(response.urljoin(src), callback=self.save_file)

        pagename = '%d-%s' % (next(self.int_gen), response.css('title::text').extract_first().encode('utf8'))
        self.logger.info("Got: {}".format(pagename))
        with open('site/{}.html'.format(pagename), 'wb') as f:
            f.write(response.body)

    def save_file(self, response):
        FTYPES = {
            'css': 'site/static/css',
            'js': 'site/static/js',
            'ico':  'site/static/img',
            'png':  'site/static/img',
            'jpg':  'site/static/img',
            'gif':  'site/static/img',
        }
        filename = response.url.split('/')[-1]
        filepath = FTYPES.get(filename.split('.')[-1])
        if filepath is not None:
            with open('/'.join((filepath, filename)), 'wb') as f:
                f.write(response.body)
        else:
            self.logger.info("Unprocessed link: {}".format(response.url))

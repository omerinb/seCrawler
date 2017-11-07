__author__ = 'tixie'
from scrapy.spiders import Spider
from seCrawler.common.searResultPages import searResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import  Selector
import json
import urllib
from bs4 import BeautifulSoup
from lxml import html 
from flask import Flask, jsonify, abort



class keywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['google.com']
    start_urls = ['https://www.google.com/search?q={0}&start={1}']
    keyword = None
    searchEngine = None
    selector = None

   
    def __init__(self, keyword, se, pages,  *args, **kwargs):
        super(keywordSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword.lower()
        self.searchEngine = se.lower()
        self.selector = SearchEngineResultSelectors[self.searchEngine]
        pageUrls = searResultPages(keyword, se, int(pages))
        for url in pageUrls:
            print(url)
            self.start_urls.append(url)

    def parse(self, response):
        
        for sel in response.xpath('//div[@class="rc"]'):
            data = {}
            data['url'] = sel.xpath('.//h3/a/@href').extract_first()
            data['title'] = sel.xpath('.//h3/a/span/text()').extract_first()
            data['picture'] = sel.xpath('.//div[@class="s"]/div/div/a/g-img/img/@src').extract_first()
            data['description'] = ""
            for res in sel.xpath('.//div[@class="s"]/div/span[@class="st"]/span//text()').extract():
                data['description'] += res
            json_data = json.dumps(data)
            yield {'url':json_data}

        pass


   
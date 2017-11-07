from scrapy.spiders import Spider
from seCrawler.common.searResultPages import searResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import  Selector
import json
import urllib
from bs4 import BeautifulSoup
from lxml import html 
from flask import Flask, jsonify, abort


class Search(resource.Resource):
	isLeaf = True
	def render_GET(self, request):
	    args = request.args

	    added_images_url=False
	    count_results =0
	    # here we want to get the value of user (i.e. ?user=some-value)
	    if b'keyword' not in  args:
	        request.setResponseCode(400)
	        return bytes('no keyword param','utf-8')
	    if b'search_engine' not in  args:
	        request.setResponseCode(400)
	        return bytes('no search_engine param','utf-8')
	    if b'num_of_results' not in  args:
	        request.setResponseCode(400)
	        return bytes('no num_of_results param','utf-8')

	    keyword,search_engine,num_of_results = self.decode_values_from_dict(args)
	    process = CrawlerRunner({
	        'USER_AGENT':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
	        'FEED_FORMAT':'json',
	        'FEED_URI':'search_results.json',
	        'ITEM_PIPELINES':{'BingCrawler.main.MyPipeline': 1}
	        })
	    if os.path.isfile(FILE_NAME):
	        os.remove(FILE_NAME)



	    process.crawl(KeywordSpider,keyword=keyword,se = search_engine,\
	                  pages=(int(math.ceil(int(num_of_results)/NUMBER_OF_RESULTS_PER_SEARCH_ENGINE[search_engine.upper()]))))


	    process.start()
	    json_file = open(FILE_NAME,'r').read()
	    json_obj_items = json.loads(json_file)
	    result_items = [item for item in json_obj_items if 'images_url' not in item]
	    image_item = [item for item in json_obj_items if 'images_url' in item]
	    result_item_requested_amount = result_items[0:int(num_of_results)]
	    result_item_requested_amount.extend(image_item)   
	    return json.dumps(result_item_requested_amount)
	       
	def decode_values_from_dict(self,args):
	  	return args[b'keyword'][0].decode('utf-8'),args[b'search_engine'][0].decode('utf-8'),args[b'num_of_results'][0].decode('utf-8')

root = Search()
factory = server.Site(root)
reactor.listenTCP(8080, factory)
reactor.run()
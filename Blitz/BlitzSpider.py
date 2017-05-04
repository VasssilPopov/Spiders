# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from sys import exit, path
# path.append('/home/peio/dev/Scrapy')
path.append('C:\STUDY_SPIDERS\Spiders\Library')
from ScrapingHelpers import *
from datetime import date, timedelta
from scrapy.selector import HtmlXPathSelector

# '$ scrapy crawl Dnevnik -o Dnevnik.json -t jsonlines'
# scrapy runspider BlitzSpider.py -o Blitz-03-May-2017.json -t json

'Get the yesterday date'
# yesterday = date.today() - timedelta(1)
today = date.today()
Today = today.strftime("%d-%b-%Y")
# Today = (date.today()).strftime("%Y-%m-%d")

class BlitzSpider(scrapy.Spider):
	name = 'Blitz'
	allowed_domains = ['www.blitz.bg']
	start_urls = [
		"www.blitz.bg/politika"
    ]
	custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

	def __init__(self):

		self.urls = ["http://www.blitz.bg/politika","http://www.blitz.bg/obshtestvo"]
		#[  'http://www.dnevnik.bg/allnews/today/']
		self.json_datafile = 'Blitz-'+Today+'.json'
		self.links_seen = self.get_ids(self.json_datafile)
		
	def get_ids(self, json_datafile):
		ids = []
		
		try:
			ids = read_ids(json_datafile)
		except (IOError,ValueError):
			return set(ids)

		return set(ids)

	def start_requests(self):
		for url in self.urls:
			yield scrapy.Request(url=url, callback=self.parse)    

	def parse(self, response):
	
		hxs = HtmlXPathSelector(response)
		qqq = hxs.select("/html/head/link[@type='application/rss+xml']/@href").extract()
		print '>>> '
		print qqq
	
		# 'We need the titles, links and times to index and follow'
		# links = response.xpath("//a[@class='news_in_a']/@href").extract()
		links = response.xpath("//article/a/@href").extract()
		for link in links:
			if link not in self.links_seen:
				yield scrapy.Request(url=link, callback=self.parse_page)


	def parse_page(self, response):

		url     = response.url
		print url
		# title   = response.xpath('//div[@class="main_left"]/h1/text()').extract()[0].strip()
		title   = response.xpath('//header/h1[@class="post-title"]/text()').extract()[0].strip()
		introStr = response.xpath('//div[@class="intro"]/text()').extract()[0].strip()
 		article = introStr.join(response.xpath('//div[@id="articleContent"]/text()').extract()).strip()

		yield {
			'url': url,
			'title': title,
			'text': article

		}	

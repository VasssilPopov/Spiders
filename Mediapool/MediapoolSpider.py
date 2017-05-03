# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from sys import exit, path
# path.append('/home/peio/dev/Scrapy')
path.append('C:\STUDY_PYTHON\Projects\LIBRARIES')
from ScrapingHelpers import *
from datetime import date, timedelta

# '$ scrapy crawl Dnevnik -o Dnevnik.json -t jsonlines'
# scrapy runspider MediapoolSpider.py -o Mediapool-30-Apr-2017.json -t json

'Get the yesterday date'
# yesterday = date.today() - timedelta(1)
today = date.today()
Today = today.strftime("%d-%b-%Y")

class MediapoolSpider(scrapy.Spider):
	name = 'Mediapool'
	allowed_domains = ['mediapool.bg', 'www.mediapool.bg']
	custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

	def __init__(self):

		self.urls = ["http://mediapool.bg/today.html"]
		#[  'http://www.dnevnik.bg/allnews/today/']
		self.json_datafile = 'Mediapool-'+Today+'.json'
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
		# 'We need the titles, links and times to index and follow'

		links = response.xpath("//a[@class='news_in_a']/@href").extract()
	
		for link in links:
			if link not in self.links_seen:
				yield scrapy.Request(url=link, callback=self.parse_page)


	def parse_page(self, response):

		url     = response.url
		title   = response.xpath('//div[@class="main_left"]/h1/text()').extract()[0].strip()
 		article = ''.join(response.xpath('//div[@class="main_left"]/div/p/text()').extract()).strip()

		yield {
			'url': url,
			'title': title,
			'article': article

		}	

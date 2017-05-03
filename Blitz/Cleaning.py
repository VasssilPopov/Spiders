# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from sys import exit, path
path.append('C:\STUDY_PYTHON\PEIO\Focus\Focus\Library')
from ScrapingHelpers import *
from datetime import date, timedelta

'$ scrapy crawl Dnevnik -o Dnevnik.json -t jsonlines'
'scrapy runspider DnevnikSpider.py -o Dnevnik-28-Apr-2017.json -t json'

'Get the yesterday date'
yesterday = date.today() - timedelta(1)
Yesterday = yesterday.strftime("%d-%b-%Y")

# Dnevnik za Yesterday
json_datafile = 'Dnevnik-'+Yesterday+'.json'

check_empty(json_datafile)

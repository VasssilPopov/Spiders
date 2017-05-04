@echo off
scrapy runspider DnevnikSpider.py -o Reports/Dnevnik-%1.json -t json 2> Logs/output.txt
@echo on

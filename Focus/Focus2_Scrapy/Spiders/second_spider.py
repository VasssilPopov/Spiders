import scrapy

class focusNews2Spider(scrapy.Spider):
    name = "focusNews2"
    allowed_domains = ["focus-news.net"]
    start_urls = [
        "http://focus-news.net/news/Yesterday/",
    ]

    def parse(self, response):
        # filename = response.url.split("/")[-2] + '.html'
        # with open(filename, 'wb') as f:
            # f.write(response.body)
			
		#'We need the titles, links and times to index and follow'

		titles = response.css('a.cnk-title::text').extract()
		titles = list( map (lambda str: str.strip(), titles) )
		
		cnt=0
		
		try
			for title in titles:
				print title
				i =i + 1
		except:
			print i
			i =i + 1
		links  = response.css('a.cnk-title::attr(href)').extract()
		links  = list( map(lambda str:'http://focus-news.net/'+str[2:], links) )
		

		times  = response.css('span.date::text').extract()
		times  = list( map(lambda str:str.split('|')[0], times) )
		
	
		for link in links:
			if link not in self.links_seen:
				# yield scrapy.Request(url=link, callback=self.parse_page)
				self.logger.info('Calling follow on %s', link)
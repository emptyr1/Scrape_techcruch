__author__ = 'Mudit uppal'


import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from clearmobtest.items import *
from scrapy.crawler import CrawlerProcess


class TechCrunchSpider(CrawlSpider):
    """
    Used to scrape content from techcurnch.com
    Several methods include:
    - getting links and yielding them
    - for each port scrape its content
    - Do some NLP to extract names and organizations - Do entity recognition
    - Repeat above steps
    """

    name = "techcrunch_spider"
    allowed_domains = ["techcrunch.com"]
    start_urls = [
        "http://techcrunch.com/"
    ]
    count = 0
    rules = (
        Rule(SgmlLinkExtractor(allow=('(.*)/(\d+)/(\d+)/(\d+)/(.*)',)), callback='parse_details'),
    )

    def parse_details(self, response):
        sel = Selector(response)
        self.count += 1
        article = Article()
        article['title'] = sel.css(".tweet-title").extract()
        article['body'] = sel.css(".article-entry").extract()
        article['url'] = response.url

        return article


#process = CrawlerProcess()
#process.crawl(TechCrunchSpider)
#process.start() # the script will block here until all crawling jobs are finished
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import FirmItem
from datetime import datetime


class FirmsSpider(CrawlSpider):
    name = "firms"
    allowed_domains = ["tubiba.com.tr"]
    start_urls = ["https://tubiba.com.tr/liste/firma"]
    #
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//ul[@class="pagination"]//a[@aria-label="Next"]',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="card blog"]/a',)), callback="parse_items", follow= False),
    )
    #
    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = FirmItem()
        item["link"] = response.request.url
        item["source"] = "tubiba"
        #
        firm_name  = hxs.xpath('//h1[@itemprop="name"]//text()').extract()
        address       = hxs.xpath('//span[@itemprop="address"]//text()').extract()
        phone          = hxs.xpath('//p[@class="summary"]//text()').extract()
        details         = hxs.xpath('//amp-accordion[contains(@class,"container")]//text()').extract()
        item["name"] = "".join(firm_name)
        item["address"] = "".join(address)
        item["tel"] = "|".join(phone)
        # item["email"] = "|".join(details)
        #
        return(item)

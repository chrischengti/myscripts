from scrapy import Spider
from scrapy.selector import Selector
from stack.items import StackItem



class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["indiatimes.com"]
    start_urls = [
        "http://economictimes.indiatimes.com/tech/software",
    ]
    def parse(self, response):
        questions = Selector(response).xpath('//*[@id="netspidersosh"]/header/div[1]/div[1]/h3')
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item


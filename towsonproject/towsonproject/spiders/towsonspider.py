import scrapy
from towsonproject.items import TowsonprojectItem

class TowsonspiderSpider(scrapy.Spider):
    name = 'towsonspider'
    allowed_domains = ['towsontigers.com']
    start_urls = ['https://towsontigers.com/']

    def parse(self, response):
        result = response.css('div > .hide')
        result1 = result.xpath('//a[contains(@href, "/roster.aspx?")]')
        result2 = result1.css('a::attr(href)').getall()
        for i in range(len(result2)):
            next_url = ('https://towsontigers.com{}').format(result2[i])
            yield response.follow(next_url, callback = self.parse_detail)
        
    def parse_detail(self,response):
        result = response.xpath('//*[@id="sidearm-roster-coaches"]/ul/li')
        item = TowsonprojectItem()
        item['sport'] = response.xpath('//*[@id="sidearm-roster-coaches"]/h3/text()').get()
        for i in range(len(result)):
            result1 = result[i].css('div.sidearm-roster-coach-details')
            if result1:
                item['name'] = result1.css('div.sidearm-roster-coach-name > p::text').get()
                item['title']= result1.css('div.sidearm-roster-coach-title > span::text').get()
                item['url']= ('https://towsontigers.com{}').format(result1.css('div.sidearm-roster-coach-link > a::attr(href)').get())
                yield item

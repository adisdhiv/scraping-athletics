import scrapy
from bsuproject.items import BsuprojectItem

class BsuspiderSpider(scrapy.Spider):
    name = 'bsuspider'
    allowed_domains = ['ballstatesports.com']
    start_urls = ['https://ballstatesports.com/']

    def parse(self, response):
        result = response.css('div >nav > .hide')
        result1 = result.xpath('//a[contains(@href, "/index.aspx?")]')
        result2 = result1.css('a::attr(href)').getall()
        sportslist = list(set(result2))
        prefix = '/index'
        filteredsports = list(filter(lambda x: x.startswith(prefix), sportslist))
        filteredsportslist = [w.replace('index', 'coaches') for w in filteredsports]
        for i in range(len(filteredsportslist)):
            next_url = ('https://ballstatesports.com/{}').format(filteredsportslist[i])
            yield response.follow(next_url, callback = self.parse_detail)

    def parse_detail(self,response):
        result3 = response.css('#main-content > article > table > tbody > tr')
        item = BsuprojectItem()
        item['sport'] = response.css('#main-content > article > h2::text').get()
        for row in result3:
            item['name'] = row.css('th > a::text').get()
            item['title']= row.xpath('td[2]//text()').extract_first().strip()
            item['phone']= row.xpath('td[3]//a//text()').extract_first()
            item['email']= row.xpath('td[4]//a//text()').extract_first()
            item['nameurl']= ('https://ballstatesports.com{}').format(row.css('th > a::attr(href)').extract_first())
            yield item

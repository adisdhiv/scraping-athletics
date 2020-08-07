import scrapy
from arizonastateunivproject.items import ArizonastateunivprojectItem

class ArizstateunivspiderSpider(scrapy.Spider):
    name = 'arizstateunivspider'
    allowed_domains = ['thesundevils.com']
    start_urls = ['https://thesundevils.com/']

    def parse(self, response):
        result = response.css('div > .hide')
        result1 = result.xpath('//a[contains(@href, "/index.aspx?")]')
        result2 = result1.css('a::attr(href)').getall()
        sportslist = list(set(result2))
        prefix = '/index'
        filteredsports = list(filter(lambda x: x.startswith(prefix), sportslist))
        filteredsportslist = [w.replace('index', 'coaches') for w in filteredsports]
        for i in range(len(sportslist)):
            next_url = ('https://thesundevils.com{}').format(filteredsportslist[i])
            yield response.follow(next_url, callback = self.parse_detail)
    
    def parse_detail(self,response):
        print(response.body)
        result3 = response.css('#main-content > article > table > tbody > tr')
        item = ArizonastateunivprojectItem()
        item['sport'] = response.css('#main-content > article > h2::text').get()
        for row in result3:
            item['name'] = row.css('th > a::text').get()
            item['title']= row.xpath('td[1]//text()').extract_first().strip()
            item['phone']= row.xpath('td[2]//a//text()').extract_first()
            item['email']= row.xpath('td[3]//a//text()').extract_first()
            item['nameurl']= ('https://thesundevils.com{}').format(row.css('a::attr(href)').extract_first())
            yield item


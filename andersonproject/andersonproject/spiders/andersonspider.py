import scrapy
from andersonproject.items import AndersonprojectItem

class AndersonspiderSpider(scrapy.Spider):
    name = 'andersonspider'
    allowed_domains = ['athletics.anderson.edu']
    start_urls = ['https://athletics.anderson.edu/']

    def parse(self, response):
        xpath = ['//*[@id="nav"]/ul/li[1]', '//*[@id="nav"]/ul/li[2]']
        category = ['Men', 'Women']
        for i in range(len(xpath)):
            result = response.xpath(xpath[i])
            list1 = result.css('div > ul')
            sportslink = list1.css('a::attr(href)').getall()
            categorynew = category[i]
            filteredsportslink = [k for k in sportslink if 'roster' in k]
            for i in range(len(filteredsportslink)):
                next_url = "https://athletics.anderson.edu" + filteredsportslink[i]
                yield response.follow(next_url, meta = {'category' : categorynew}, callback = self.parse_detail)

    def parse_detail(self,response):
        item = AndersonprojectItem()
        item['sport'] = response.xpath('//*[@id="mainbody"]/div[1]/div[4]/div/div/div/div[1]/h1/text()').get()
        item['category'] = response.meta['category']
        result = response.xpath('//*[@id="mainbody"]/div[1]/div[4]/div/div/div/div[1]/div/div')
        for i in range(len(result)):
            result1 = result[i].css('.span6')
            for i in range(len(result1)):
                result2 = result1[i].css('.info')
                item['url'] = ('https://athletics.anderson.edu{}').format(result2.css('p > a::attr(href)').get())
                item['imgurl'] = ('https://athletics.anderson.edu{}').format(result2.css('p > a > img::attr(src)').get())
                item['name'] = result2.css('p > a > span::text').get()
                item['title'] = result2.css('p:nth-child(2)::text').get()
                item['phone'] = result2.css('p:nth-child(4)::text').get()
                item['email'] = result2.css('p.email > a::text').get()
                yield(item)
            
    


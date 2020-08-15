import scrapy
from fullertonproj.items import FullertonprojItem


class FullertonspiderSpider(scrapy.Spider):
    name = 'fullertonspider'
    allowed_domains = ['fullertontitans.com']
    start_urls = ['https://fullertontitans.com/']

    def parse(self, response):
        page = response.xpath('//*[@id="submenu1"]')
        sportslink = page.css('li > a::attr(href)').getall()
        sport = page.css('li > a::text').getall()
        sportslink = sportslink[:-3]
        for i in range(len(sportslink)):
            nexturl = "https://fullertontitans.com" + sportslink[i].replace('index',"") + "coaches/index"
            yield response.follow(nexturl, meta = {'urls' : nexturl, 'sport' : sport[i]}, callback = self.parse_detail)

    def parse_detail(self,response):
        page = response.xpath('//*[@id="mainbody"]/div[1]/div[1]/select')
        optionvalue = page.css('option::attr(value)').getall()
        urls1 = []
        urls1.append(response.meta['urls'])
        sport = response.meta['sport']
        for i in optionvalue:
            optionlink = "https://fullertontitans.com" + i
            urls1.append(optionlink)
        for i in urls1:
            yield response.follow(i, meta = {'urls' : i,'sport' : sport}, callback = self.parse_details)

    def parse_details(self,response):
        item = FullertonprojItem()
        item['url'] = response.meta['urls']
        item['sport'] = response.meta['sport']
        item['name'] = response.xpath('//*[@id="mainbody"]/div[1]/div[2]/div/div/div[2]/div/span/text()').getall()
        table = response.xpath('//*[@id="mainbody"]/div[1]/div[2]/div/div/div[2]/table')
        for i in table:
            row = i.css('tr')
            list1 = []
            for i in range(len(row)):
                keys = row[i].css('td.label::text').getall()
                k = row[i].css('td.value::text').getall()
                j = row[i].css('td.value > a::text').getall()
                values = k+j
                list1.append(dict(zip(keys, values)))

            for li in range(len(list1)):
                try:
                    item['phone'] = list1[li]['Phone: ']
                except KeyError:
                    pass
                try:
                    item['email'] = list1[li]['Email: ']
                except KeyError:
                    pass
                try:
                    item['position'] = list1[li]['Position: ']
                except KeyError:
                    pass
            yield item




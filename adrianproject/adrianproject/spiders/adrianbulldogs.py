import scrapy
from adrianproject.items import AdrianprojectItem

class AdrianbulldogsSpider(scrapy.Spider):
    name = 'adrianbulldogs'
    allowed_domains = ['adrianbulldogs.com']
    start_urls = ['https://adrianbulldogs.com/']

    def parse(self, response):
        xpath = ['//*[@id="nav"]/ul/li[1]', '//*[@id="nav"]/ul/li[2]']
        category = ['Men', 'Women']
        for i in range(len(xpath)):
            result = response.xpath(xpath[i])
            list1 = result.css('div > ul')
            sportslink = list1.css('a::attr(href)').getall()
            sportslist = list1.css('a::attr(aria-label)').getall()
            categorynew = category[i]
            filteredsportslink = [k for k in sportslink if 'coaches' in k]
            filteredsportslist = [k for k in sportslist if 'Coaches' in k]
            for i in range(len(filteredsportslink)):
                if filteredsportslink[i].startswith('http'):
                    pass
                else:
                    filteredsportslink[i] = 'https://adrianbulldogs.com' + filteredsportslink[i] 
            for i in range(len(filteredsportslink)):
                next_url = filteredsportslink[i]
                sport = filteredsportslist[i]
                yield response.follow(next_url, meta = {'sport' : sport, 'category' : categorynew}, callback = self.parse_detail)

        
    def parse_detail(self,response):
        result = response.xpath('//*[@id="mainbody"]/div[1]/div/div')
        sport = response.xpath('//*[@id="mainbody"]/div[1]/h1/text()').get()
        item = AdrianprojectItem()
        itemdummy = sport
        item['sport'] = sport
        if itemdummy:
            if "Men's and Women's" in itemdummy:
                item['category'] = "Both"
            else:
                item['category'] = response.meta['category']
        for i in range(len(result)):
            result1 = result[i].css('.span6')
            for i in range(len(result1)):
                result2 = result1[i].css('.info')
                item['url'] = result2.css('p > a::attr(href)').get()
                item['imgurl'] = result2.css('p > a > img::attr(src)').get()
                item['name'] = result2.css('p > a > span::text').get()
                item['title'] = result2.css('p:nth-child(2)::text').get()
                item['phone'] = result2.css('p:nth-child(4)::text   ').get()
                item['email'] = result2.css('p.email > a::text').get()
                yield(item)

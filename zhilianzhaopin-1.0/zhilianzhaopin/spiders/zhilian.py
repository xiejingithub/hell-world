# -*- coding: utf-8 -*-
import scrapy
from zhilianzhaopin.items import ZhilianzhaopinItem
import re
from urllib import parse
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ZhilianSpider(CrawlSpider):
    name = 'zhilian'
    allowed_domains = ['www.zhaopin.com']
    start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=python&sm=0&isfilter=0&fl=530&isadv=0&sg=54f538cbe96f4209a145a49cf5fd5f46&p=1']


    # rules = (
    #     Rule(LinkExtractor(allow=('jobs.zhaopin.com/[0-9]*\.htm',)),callback='parse_one_job',follow=True),
    #     Rule(LinkExtractor(allow=('jobs.zhaopin.com/[0-9]*\.htm',),deny=('[a-zA-Z0-9]*/in[0-9]*_','zhaopin.liebiao.com',
    #                                                 'jobs.zhaopin.com/[a-z]*/[a-z0-9]*/[a-z0-9_]*')),follow=True),
    # )


    # def parse(self, response):
    #     city_list = ['北京','上海','广州','深圳','天津','武汉','西安','成都','大连','长春','沈阳','南京',
    #                  '济南','青岛','杭州','苏州','无锡','宁波','重庆','郑州','长沙','福州','厦门','哈尔滨',
    #                  '石家庄','合肥','惠州']
    #     post_list = ['python','java','爬虫','hadoop','大数据']
    #     for city in city_list:
    #         for post in post_list:
    #             url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl='+city+'&kw='+post+'&p=1&isadv=0'
    #             if city and post:
    #                 yield Request(url=url,callback=self.parse_dispose_url,dont_filter=True,headers=self.headers)


    def parse(self, response):
        post_urls = response.xpath('//*[@id="newlist_list_content_table"]//td[@class="zwmc"]//a[1]/@href').extract()
        if post_urls:
            for post_url in post_urls:
                yield Request(url=post_url, callback=self.parse_detail, dont_filter=True)

        next_url = response.css('.newlist_wrap.fl .pagesDown .pagesDown-pos a::attr(href)').extract()
        if next_url:
            next_url = response.css('.newlist_wrap.fl .pagesDown .pagesDown-pos a::attr(href)').extract()[0]
            yield Request(url=next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        url = response.url
        title = response.css('.top-fixed-box .fixed-inner-box h1::text').extract()[0]
        company = response.css('.top-fixed-box .fixed-inner-box h2 a::text').extract()[0]
        salary = response.css('.terminalpage.clearfix strong::text').extract()[0].strip()
        if salary == '面议':
            salary_min = '面议'
            salary_max = '面议'
        else:
            salary_min = int(re.findall('(.{4,6})-.{4,6}.*', salary)[0])
            salary_max = int(re.findall('.{4,6}-(.{4,6})元.*', salary)[0])
        start_date = str(response.xpath('//*[@id="span4freshdate"]/text()').extract()[0])
        experience = response.xpath('/html/body/div[6]/div[1]/ul/li[5]/strong/text()').extract()[0]
        count = int(response.xpath('/html/body/div[6]/div[1]/ul/li[7]/strong/text()').extract()[0].replace('人','').strip())
        site = response.css('.tab-cont-box .tab-inner-cont h2::text').extract()[0].strip()
        nature = response.xpath('/html/body/div[6]/div[1]/ul/li[4]/strong/text()').extract()[0]
        edu = response.xpath('/html/body/div[6]/div[1]/ul/li[6]/strong/text()').extract()[0]
        type = response.xpath('/html/body/div[6]/div[1]/ul/li[8]/strong/a/text()').extract()[0]
        print (url,title,company,salary_min,salary_max,start_date,experience,count,site,nature,edu,type)
        # people_num =  response.css('.terminalpage.clearfix strong::text').extract()[6]
        # people_min = int(re.findall('(.{1,6})-.{1,6}人',people_num))
        # people_max = int(re.findall('.{1,6}-(.{1,6})人', people_num))
        # people_num = int((people_max+people_min)/2)

        zhilian = ZhilianzhaopinItem()
        zhilian['url'] = url
        zhilian['title'] = title
        zhilian['company'] = company
        zhilian['salary_min'] = salary_min
        zhilian['salary_max'] = salary_max
        zhilian['start_date'] = start_date
        zhilian['experience'] =experience
        zhilian['count'] = count
        zhilian['site'] = site
        zhilian['nature'] = nature
        zhilian['edu'] = edu
        zhilian['type'] = type

        yield  zhilian
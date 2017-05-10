# -*- coding: utf-8 -*-
import scrapy,re
from jobStat.items import workDetails

class TestSpider(scrapy.Spider):
    name = "jobs51"
    allowed_domains = ["51job.com"]
    start_urls = ["http://m.51job.com/search/joblist.php?jobarea=010000&issuedate=0"]
    #item=workDetails()

    #def start_requests(self):
    #    yield scrapy.Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        results=response.xpath("//p[@class='result']").re("(\d+)")[0]
        pages=int(int(results)/30)
        for i in range(pages):
            url='http://m.51job.com/search/joblist.php?jobarea=010000&issuedate=0&pageno=%d'%i
            yield scrapy.Request(url,callback=self.parse_url)

    def parse_url(self,response):
        href = response.xpath("//div[@class='jblist res']/a")
        for h in href:
            url=h.xpath("./@href").extract()[0]
            yield scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self,response):
        #item=workDetails()
        meta={}
        meta['url']=response.url
        meta['jobid']=re.findall(r'&jobid=(\d+)',response.url)[0]
        meta['workName'] = response.xpath("//p[@class='xtit']/text()").extract()[0]


        Details=response.xpath("//div[@class='xqd']/label/text()")
        meta['comType'] = Details[0].extract()

        salary=Details[2].extract().strip()
        #item['salary']=salary
        p = "(\d+(?:\.\d+)?)(?:\-(\d+(?:\.\d+)?))?(\w+)\/(\w+)"
        s=re.findall(p,salary,re.U)
        if len(s[0])==4:
            aver_s=(float(s[0][0])+float((s[0][1] if s[0][1]!='' else 0)))/2
            if s[0][2]==u"千":
                aver_s *= 1000
            elif s[0][2]==u"万":
                aver_s *= 10000
            elif s[0][2]==u"百":
                aver_s *= 100

            if s[0][3]==u"年":
                aver_s /= 12
            elif s[0][3]==u"时":
                aver_s *= 8*20.9
            elif s[0][3]==u"天":
                aver_s *= 20.9
            meta['salary']=aver_s
        else:
            meta['salary']=salary

        Content=Details[5].extract().strip().split('|')
        meta['degree']=Content[1]
        meta['workYears']=Content[2]
        meta['comName']=response.xpath("//a[@class='xqa']/text()").extract()[0]
        comUrl=response.xpath("//a[@class='xqa']/@href").extract()[0]
        #print meta
        yield scrapy.Request(comUrl,meta=meta,callback=self.parse_industry)

    def parse_industry(self,response):
        item=workDetails()
        meta=response.meta
        item['url']=meta['url']
        item['workName'] = meta['workName']
        item['salary'] = meta['salary']
        item['workYears'] = meta['workYears']
        item['degree'] = meta['degree']
        item['jobid'] = meta['jobid']
        item['comType'] = meta['comType']
        item['comName'] = meta['comName']
        item['comIndustry']=response.xpath("//aside[@class='ldes ']/p/font/text()")[2].extract()
        #print item
        return item

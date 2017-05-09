# -*- coding: utf-8 -*-
import scrapy,re
from jobStat.items import workDetails

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["51job.com"]
    start_urls = ["http://search.51job.com/list/010000,000000,0000,00,0,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="]

    def parse(self, response):
        pages=response.xpath('//div[@class="p_in"]/span/text()')[0].re(u'共(\d+)页')
        pages=int(pages[0])
        for i in range(1,pages+1):
            yield scrapy.Request("http://search.51job.com/list/010000,000000,0000,00,0,99,%2B,2,"+str(i)+".html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",\
                                 callback=self.parse_url)

    def parse_url(self,response):
        for u in response.xpath('//div[@class="el"]/p/span/a/@href').extract():
            searchUrl=re.findall(r'/(\d+).html',u)[0]
            yield scrapy.Request(searchUrl,callback=self.parse_detail)

    def parse_detail(self,response):
        item=workDetails()
        inbox=response.xpath('//div[@class="jtag inbox"]/div')
        item['url']=response.url
        item['jobid']=re.findall(r'/(\d+).html',response.url)[0]

        item['workName']=response.xpath('//div[@class="tHeader tHjob"]/div/div/h1/@title').extract()[0]

        salary=response.xpath('//div[@class="tHeader tHjob"]/div/div/strong/text()').extract()[0]
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
            item['salary']=aver_s    
        else:
            item['salary']=salary

        workYears=inbox.xpath('./span/text()')[0].re(u"([\w\-.]+经验)")
        if len(workYears)==0:
            item['workYears']=u"无工作经验"
        else:
            item['workYears']=workYears[0]

        degree=inbox.xpath('./span/text()')[1].re(u"(初中及以下|中技|高中|中专|大专|本科|硕士|博士)")
        if len(degree)==0:
            degree = inbox.xpath('./span/text()')[0].re(u"(初中及以下|中技|高中|中专|大专|本科|硕士|博士)")
            if len(degree)==0:
                item['degree']=u"学历不限"
            else:
                item['degree'] = degree[0]
        else:
            item['degree']=degree[0]

        item['jobType']=response.xpath('//p[@class="msg ltype"]/text()').extract()[0].split('|')[2].strip()
        return item
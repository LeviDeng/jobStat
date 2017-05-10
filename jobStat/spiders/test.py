# -*- coding: utf-8 -*-
import scrapy,re
from jobStat.items import workDetails

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["51job.com"]
    start_urls = ["http://search.51job.com/list/010000,000000,0000,00,0,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="]
    headers={
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    cookies={'nsearch': 'jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D', 'search': 'jobarea%7E%60010000%\
7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA0%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB\
%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1493883998%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1\
%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1493881686%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch2%7E%601%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1\
%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA0%A1%FB%A1%FA99%A1%FB%A1%FA01%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1493884023%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%F\
A%7C%21collapse_expansion%7E%601%7C%21', 'ps': 'us%3DWWdROwZ6AjVdOAxpBn1TYgAwBjBTewdgAjYBYFwqBDUAPAdlDmgANVY%252BWjZVNlNoATYAMgYwWztULgYHAWpUHVkJUXk%253D%26%7C%26needv%3D0', '_ujz': 'NDg1ODMwMjUw', '51job': 'cuid%3D48583025%26%7C%26c\
username%3Dptrees%26%7C%26cpassword%3D%26%7C%26cname%3D%25B5%25CB%25C1%25D6%26%7C%26cemail%3Dptrees%2540sina.cn%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.00wI4dWyrWmw%26%7C%26cconfirmkey%3DptuBFHmpk4hTA%26%7C%26cr\
esumeids%3D.0ODsb3S8YKGw%257C%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DptyV.5hr5%252F5VU%26%7C%26to%3DDzMGZQ5pBTtRMwllVzBRZ1QrBXRSIFJ1UTJdag92AHwLMlE%252FD28HNFc%252FWjQCYVNnBTRWYg%253D%253D%26%7\
C%26', 'slife': 'lastvisit%3D010000%26%7C%26lowbrowser%3Dnot', 'partner': '51jobhtml5', 'guid': '14943210294081740036'}
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301,302]  # 对哪些异常返回进行处理
    }

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse, cookies=self.cookies,\
                      headers=self.headers, meta=self.meta)

    def parse(self, response):
        pages=response.xpath('//div[@class="p_in"]/span/text()')[0].re(u'共(\d+)页')
        pages=int(pages[0])
        for i in range(1,pages+1):
            url='http://search.51job.com/list/010000,000000,0000,00,0,99,%2B,2,'+str(i)+'.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
            yield scrapy.Request(url,cookies=self.cookies,headers=self.headers, meta=self.meta,callback=self.parse_url)

    def parse_url(self,response):
        for u in response.xpath('//div[@class="el"]/p/span/a/@href').extract():
            searchUrl=re.findall(r'/(\d+).html',u)[0]
            yield scrapy.Request(searchUrl,ookies=self.cookies,\
                      headers=self.headers, meta=self.meta,callback=self.parse_detail)

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
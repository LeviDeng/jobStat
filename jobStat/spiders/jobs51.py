# -*- coding: utf-8 -*-
import scrapy,re,time
from jobStat.items import workDetails
import requests
from lxml import etree
from time import sleep
import pymongo

class TestSpider(scrapy.Spider):
    name = "jobs51"
    #allowed_domains = ["51job.com"]
    start_urls = ["http://m.51job.com/search/joblist.php?jobarea=010000&issuedate=0"]
    jobIDs=[]
    jobidFile="jobIDs_2017-05-17.txt"
    #item=workDetails()

    #def start_requests(self):
    #    yield scrapy.Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        results=response.xpath("//p[@class='result']").re("(\d+)")[0]
        pages=int(int(results)/30)
        jobids=self.get_jobid_from_file(self.jobidFile)
        #self.get_jobid(pages)
        #jobids=self.jobIDs
        for j in jobids:
            u="http://m.51job.com/search/jobdetail.php?jobtype=0&jobid=%d"%int(j.strip())
            yield scrapy.Request(u,callback=self.parse_detail)

    def get_jobid_from_file(self,filename):
        f=open(filename)
        content=f.readlines()
        return content

    def get_jobid(self,pages):
        for i in range(pages):
            url='http://m.51job.com/search/joblist.php?jobarea=010000&issuedate=0&pageno=%d'%i
            res=requests.get(url)
            html=etree.HTML(res.text)
            href = html.xpath("//div[@class='jblist res']/a")
            for h in href:
                u = h.xpath("./@href")[0]
                jobid = re.findall(r'&jobid=(\d+)', u)[0]
                self.jobIDs.append(int(jobid))
        with open("jobIDs_%s.txt"%time.strftime("%Y-%m-%d",time.localtime()),'w') as f:
            for j in self.jobIDs:
                f.write(str(j)+'\n')


    '''
    def parse_url(self,response):
        href = response.xpath("//div[@class='jblist res']/a")
        coll=pymongo.MongoClient('localhost',27017)['jobs51']['jobs']
        for h in href:
            url=h.xpath("./@href").extract_first()
            jobid=re.findall(r'&jobid=(\d+)',url)[0]
            self.jobIDs.append(int(jobid))
            #if coll.find({"jobid":jobid}).count()==0:
            yield scrapy.Request(url,callback=self.parse_detail)
    '''
    def parse_detail(self,response):
        #item=workDetails()
        item = workDetails()
        con=pymongo.MongoClient('localhost',27017)
        coll=con['jobs51']['coms']
        #meta={}
        item['url']=response.url
        item['jobid']=re.findall(r'&jobid=(\d+)',response.url)[0]
        item['workName'] = response.xpath("//p[@class='xtit']/text()").extract_first()

        Details=response.xpath("//div[@class='xqd']/label")
        item['comType']=item['salary']=item['degree']=item['workYears']=item['employNums']=None
        for l in Details:
            if l.xpath("./span/text()").re(u"性质"):
                item['comType'] = l.xpath("./text()").extract_first()
            if l.xpath("./span/text()").re(u"薪资"):
                salary = l.xpath("./text()").extract_first()
                # item['salary']=salary
                p = "(\d+(?:\.\d+)?)(?:\-(\d+(?:\.\d+)?))?(\w+)\/(\w+)"
                s = re.findall(p, salary, re.U)
                if len(s[0]) == 4:
                    aver_s = (float(s[0][0]) + float((s[0][1] if s[0][1] != '' else 0))) / 2
                    if s[0][2] == u"千":
                        aver_s *= 1000
                    elif s[0][2] == u"万":
                        aver_s *= 10000
                    elif s[0][2] == u"百":
                        aver_s *= 100
                    if s[0][3] == u"年":
                        aver_s /= 12
                    elif s[0][3] == u"小":
                        aver_s *= 8 * 20.9
                    elif s[0][3] == u"天":
                        aver_s *= 20.9
                    item['salary'] = aver_s
                else:
                    item['salary'] = salary
            if l.xpath("./span/text()").re(u"招聘"):
                degree=workYears=employNums=None
                Content = l.xpath("./text()").extract_first()
                try:
                    degree=re.findall(u"(初中及以下|高中|中技|中专|大专|本科|硕士|博士|学历不限)",Content,re.U)[0]
                except:
                    pass
                try:
                    workYears=re.findall(u"([^\|]+经验[^\|]+)",Content,re.U)[0]
                except:
                    pass
                try:
                    employNums=re.findall(u"(?:招聘)?(\w+)人",Content,re.U)[0]
                except:
                    pass
                item['degree'] = degree
                item['workYears'] = workYears
                try:
                    item['employNums'] = int(employNums)
                except:
                    item['employNums'] = employNums

        item['comName']=response.xpath("//a[@class='xqa']/text()").extract_first()
        comUrl=response.xpath("//a[@class='xqa']/@href").extract_first()
        coid=re.findall("coid=(\d+)",comUrl)[0]
        if coll.find({'coid':coid}):
            item['comIndustry']=coll.find({'coid':coid})[0]['comIndustry']
        else:
            sleep(3)
            res=requests.get(comUrl)
            html=etree.HTML(res.text)
            for p in html.xpath("//aside")[1].xpath("./p"):
                if re.findall(u"行业",p.xpath("./span/text()")[0].encode("raw_unicode_escape").decode("utf8"),re.U):
                    item['comIndustry'] = p.xpath("./font/text()")[0].encode("raw_unicode_escape").decode("utf8")
            coll.insert_one({
                'coid':coid,
                'comIndustry':item['comIndustry'],
                'comName':item['comName'],
            })
        item['comIND']=item['comIndustry'].split()[0]

        item['date']=time.strftime("%Y-%m-%d",time.localtime())
        return item
        #yield scrapy.Request(comUrl,meta=meta,callback=self.parse_industry,dont_filter=True)

    def parse_industry(self,response):
        item=workDetails()
        meta=response.meta
        try:
            item['url']=meta['url']
        except:
            pass
        try:
            item['workName'] = meta['workName']
        except:
            pass
        try:
            item['salary'] = meta['salary']
        except:
            pass
        try:
            item['workYears'] = meta['workYears']
        except:
            pass
        try:
            item['degree'] = meta['degree']
        except:
            pass
        try:
            item['jobid'] = meta['jobid']
        except:
            pass
        try:
            item['comType'] = meta['comType']
        except:
            pass
        try:
            item['comName'] = meta['comName']
        except:
            pass
        try:
            item['employNums'] = meta['employNums']
        except:
            pass
        try:
            item['date'] = meta['date']
        except:
            pass
        item['comIndustry']=None
        for p in response.xpath("//aside")[1].xpath("./p"):
            if p.xpath("./span/text()").re(u"行业"):
                item['comIndustry']=p.xpath("./font/text()").extract_first()

        #print item
        return item

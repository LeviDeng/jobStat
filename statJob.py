#coding:utf8
import re,pymongo

class statJob():
    con=pymongo.MongoClient('localhost',27017)
    coll=con['jobs51']['jobs']
    def getSalary(self,job):
        p = "(\d+(?:\.\d+)?)(?:\-(\d+(?:\.\d+)?))?(\w+)\/(\w+)"
        s=re.findall(p,job['salary'],re.U)
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
            elif s[0][3] == u"时":
                aver_s *= 8 * 20.9
            elif s[0][3] == u"天":
                aver_s *= 20.9
            salary=aver_s
        else:
            #print s
            salary=job['salary']
        return salary

    def writeResult(self):
        with open("statResult.txt","w") as f:
            for j in self.coll.find():
                f.write(j['workName'].encode('utf8')+":"+str(self.getSalary(j))+"\n")

#if "__name__"=="__main__":
s=statJob()
s.writeResult()
#coding:utf-8
import pymongo,re
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
#from statJob import statJob
import xlrd,xlutils.copy,xlwt,os

FILENAME="statResult.xls"

def getSalary(job):
    p = "(\d+(?:\.\d+)?)(?:\-(\d+(?:\.\d+)?))?(\w+)\/(\w+)"
    s = re.findall(p, job['salary'], re.U)
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
        salary = aver_s
    else:
        # print s
        salary = job['salary']
    return salary

class Graphs():

    def paintHistograms(self):
        data = []
        plt.hist(list(data))
        plt.xlabel("test")
        plt.show()

    def paintLine(self):
        #x = ["3000-", "3000-5000", "5000-8000", "8000-15000", "15000-40000", "40000+"]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        x=[1,2,3,4,5,6]
        y=[0,0,0,0,0,0]
        coll=pymongo.MongoClient('localhost',27017)['jobs51']['jobs']
        for j in coll.find():
            try:
                salary=getSalary(j)
            except:
                salary=j['salary']
            try:
                s=float(salary)
                if s<3000:
                    y[0] += 1
                elif s>= 3000 and s<5000:
                    y[1] +=1
                elif s>=5000 and s<8000:
                    y[2] +=1
                elif s>=8000 and s<15000:
                    y[3] += 1
                elif s>=15000 and s<30000:
                    y[4] += 1
                elif s>= 30000:
                    y[5] += 1
            except:
                print salary
                #print s
                #y.append(float(s))
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.bar(x,y)
        ax.set_xticklabels(['',u'3k以下','3k-5k','5k-8k','8k-15k','15k-30k','30k+'])
        for i,num in enumerate(y):
            ax.text(i+0.75,num,num)
        ax.set_xlabel(u"工资范围")
        ax.set_ylabel(u"人数")
        ax.set_title(u"北京招聘薪资统计")
        plt.show()

    def testText(self):
        matplotlib.rcParams['font.sans-serif'] = ['Source Han Sans ZH', 'sans-serif']
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        p = patches.Rectangle((left, bottom), width, height,\
            fill=False, transform=ax.transAxes, clip_on=False)
        ax.add_patch(p)
        ax.text(right, top, u'呵呵',
                horizontalalignment='right',
                verticalalignment='bottom',
                transform=ax.transAxes)
        x=[1,2,3,4]
        y=[2,4,8,16]

        ax.set_axis_off()
        ax.bar(x, y)
        plt.show()

    def testTick(self):
        x=[1,2,3,4]
        y=[2,4,8,16]
        plt.bar(x,y)
        plt.show()

    def testAxes(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_axes([0.1, 0.1, 0.7, 0.3])
        x=[1,2,3]
        y=[2,4,8]
        ax1.bar(x,y)
        ax1.set_xticklabels(['','','aa','','bb','','cc'])
        plt.show()

def writeExcel(filename):
    if not os.path.exists(FILENAME):
        wb=xlwt.Workbook()
        ws=wb.add_sheet("1")
        wb.save(FILENAME)
    data=xlrd.open_workbook(FILENAME)
    wdata=xlutils.copy.copy(data)
    ws=wdata.get_sheet(0)
    con=pymongo.MongoClient('localhost',27017)
    coll=con['jobs51']['jobs']
    x=[u'3k以下',u'3k-5k',u'5k-8k',u'8k-15k',u'15k-30k',u'30k+',u'总计']
    x1=[0,0,0,0,0,0]
    z={}
    for i,v in enumerate(x):
        ws.write(0,i+1,v)

    for j in coll.find():
        try:
            salary=float(j['salary'])
            enum=int(j['employNums'])
            #comIndustry = j['comIND']
            if salary < 3000:
                x1[0] += enum
                if j['comIND'] not in z:
                    z[j['comIND']] = [enum, 0, 0, 0, 0, 0]
                else:
                    z[j['comIND']][0] += enum
            elif salary > 3000 and salary <= 5000:
                x1[1] += enum
                if j['comIND'] not in z:
                    z[j['comIND']] = [0, enum, 0, 0, 0, 0]
                else:
                    z[j['comIND']][1] += enum
            elif salary > 5000 and salary <= 8000:
                x1[2] += enum
                if j['comIND'] not in z:
                    z[j['comIND']] = [0, 0, enum, 0, 0, 0]
                else:
                    z[j['comIND']][2] += enum
            elif salary > 8000 and salary <= 15000:
                x1[3] += enum
                if j['comIND'] not in z:
                    z[j['comIND']] = [0, 0, 0, enum, 0, 0]
                else:
                    z[j['comIND']][3] += enum
            elif salary > 15000 and salary <= 30000:
                x1[4] += enum
                if j['comIND'] not in z:
                    z[j['comIND']] = [0, 0, 0, 0, enum, 0]
                else:
                    z[j['comIND']][4] += enum
            elif salary > 30000:
                x1[5] += enum
                if j['comIND'] not in z:
                    z[j['comIND']] = [0, 0, 0, 0, 0, enum]
                else:
                    z[j['comIND']][5] += enum
        except :
            pass

    for i,n in enumerate(x1):
        ws.write(1,i+1,n)
    ws.write(1,7,sum(x1,0))
    sums=[0]*(len(z.keys()))
    for i,k in enumerate(z.keys()):
        ws.write(i+2,0,k)
        for j,v in enumerate(z[k]):
            ws.write(i+2,j+1,v)
            sums[i] += int(v)
    for i in range(len(z)):
        ws.write(i+2,7,sums[i])

    wdata.save(FILENAME)



g=Graphs()
#g.paintLine()
#g.testAxes()
writeExcel('statResult.xlsx')
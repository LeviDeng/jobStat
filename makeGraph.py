#coding:utf-8
import numpy as np
import pylab as pl
from statJob import statJob

class Graphs():
    def paintHistograms(self):
        data = np.random.normal(5.0, 3.0, 1000)
        pl.hist(list(data))
        pl.xlabel("test")
        pl.show()

    def paintLine(self):
        #x = ["3000-", "3000-5000", "5000-8000", "8000-15000", "15000-40000", "40000+"]
        x=[1,2,3,4,5,6]
        y=[0,0,0,0,0,0]
        with open("statResult.txt") as f:
            for v in f.readlines():
                s=v.strip().split(':')[-1]
                try:
                    s=float(s)
                    if s<3000:
                        y[0] += 1
                    elif s>= 3000 and s<5000:
                        y[1] +=1
                    elif s>=5000 and s<8000:
                        y[2] +=1
                    elif s>=8000 and s<15000:
                        y[3] += 1
                    elif s>=15000 and s<40000:
                        y[4] += 1
                    elif s>= 40000:
                        y[5] += 1
                except:
                    print v.decode('utf8')
                #print s
                #y.append(float(s))
        pl.bar(x,y)
        pl.show()

g=Graphs()
g.paintLine()
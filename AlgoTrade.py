import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time 

date,bid,ask = np.loadtxt('GBPUSD1d.txt', unpack=True, 
                                  delimiter=',', 
                                  converters={0:mdates.strpdate2num('%Y%m%d%H%M%S')}); 

patternAr = []
pAr = []
avgLine = ((bid+ask)/2)

def precentChange(startPoint, currentPoint):
        return ((float(currentPoint)-startPoint)/abs(startPoint))*100.00

def patternStorage():
        patStartTime = time.time()
        x = len(avgLine)-30
        y = 11
        while y < x:
                p = {}
                for x in xrange(11): 
                        p["p{0}".format(x)] = precentChange(avgLine[y - 10], avgLine[(x - 10) + y])

                outcomeRange = avgLine[y+20:y+30]
                currentPoint = avgLine[y]
                try:
                        avgOutcome = reduce(lambda x, y: x+y, outcomeRange) / len(outcomeRange)
                except Exception, e:
                        print str(e)
                        avgOutcome = 0

                futureOutcome = precentChange(currentPoint, avgOutcome)
                
                pattern = [p.get("p{0}".format(x)) for x in xrange(11)]
                
                patternAr.append(pattern)
                pAr.append(futureOutcome)
               
                y += 1

        patEndTime = time.time()
        print len(patternAr)
        print len(pAr)
        print 'Pattern Storage took: ', patEndTime - patStartTime, 'Seconds'

def patternRecongnition():
        cP = {}
        for x in xrange(10): 
                cP["cP{0}".format(x)] = precentChange(avgLine[-11], avgLine[x - 10])       

        patForRec = [cP.get("cP{0}".format(x)) for x in xrange(10)] 
                
        print patForRec
        

def graphRawFx(): 
        fig = plt.figure(figsize=(10,7))
        axis_1 = plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)

        axis_1.plot(date,bid)
        axis_1.plot(date,ask)
        plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

        axis_1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H: %M: %S')) 
        for label in axis_1.xaxis.get_ticklabels(): 
                label.set_rotation(45)

        axis_1_2 = axis_1.twinx()
        axis_1_2.fill_between(date, 0, (ask-bid), facecolor='g', alpha=.3)

        plt.subplots_adjust(bottom=.23) 
        
        plt.grid(True) 
        plt.show()
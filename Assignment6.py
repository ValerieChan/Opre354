
from SimPy.Simulation import *
import random
import coxian
import numpy
import math
#use coxian.coxian() for t
def conf(L):
    """95% confidence interval"""
    lower = numpy.mean(L) - 1.96*numpy.std(L)/math.sqrt(len(L))
    upper = numpy.mean(L) + 1.96*numpy.std(L)/math.sqrt(len(L))
    return (lower, upper)

## Model ----------
class Source(Process):
    """generate random arrivals"""
    def run(self, N, lamb, k):
        for i in range(N):
            a = Arrival(str(i))
            activate(a, a.run())
            t = random.expovariate(lamb)
            yield hold, self, t

class Arrival(Process):
    """an arrival"""
    n=0
    
    def run(self):
        Arrival.n += 1
        arrivetime = now()
        G.numbermon.observe(Arrival.n)
        if(Arrival.n>0):
            G.busymon.observe(1)
        else:
            G.busymon.observe(0)
        
        yield request, self, G.server
        t = coxian.coxian()
        G.servicemon.observe(t)
        G.servicesquaredmon.observe(t**2)
        yield hold, self, t
        yield release, self, G.server
        Arrival.n -= 1
        G.numbermon.observe(Arrival.n)
        if(Arrival.n>0):
            G.busymon.observe(1)
        else:
            G.busymon.observe(0)
        delay = now()-arrivetime
        G.delaymon.observe(delay)


class G:
    server = 'dummy'
    delaymon = 'Monitor'
    numbermon = 'Monitor'
    busymon = 'Monitor'
    servicemon = 'Monitor'
    servicesquaredmon = 'Monitor'
    
def model(c, N, lamb, k, maxtime, rvseed):
    # setup
    initialize()
    random.seed(rvseed)
    G.server = Resource(c, monitored = True)
    G.delaymon = Monitor()
    G.numbermon = Monitor()
    G.busymon = Monitor()
    G.servicemon = Monitor()
    G.servicesquaredmon = Monitor()
   
    # simulate
    s = Source('Source')
    activate(s, s.run(N, lamb, k))
    simulate(until=maxtime)
   
    # gather performance measures
    W = G.delaymon.mean()
    L = G.numbermon.timeAverage()
    B = G.busymon.timeAverage()
    S = G.servicemon.mean()
    S2 = G.servicesquaredmon.mean()
    LQ = G.server.waitMon.timeAverage()
    lambeff = L/W
    WQ = LQ/lambeff

    PK = ((lambeff*S2)/(2.0*(1-B)))
    y = WQ-PK
    #print PK
    #print WQ
    return(y)

## Experiment ----------------
AllY=[]
for i in range(50):
    seed = 123*i
    result = model(c=1, N=10000, lamb=1, k=2,
               maxtime=2000000, rvseed=seed)
    AllY.append(result)
print ""
print "Estimate of Y:", numpy.mean(AllY)
print "Conf of Y:", conf(AllY)

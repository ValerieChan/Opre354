"""(q4.py) M/M/c queueing system with several monitors and multiple replications"""

from SimPy.Simulation import *
import random
import numpy
import math

## Useful extras ----------
def conf(L):
    """confidence interval"""
    lower = numpy.mean(L) - 1.96*numpy.std(L)/math.sqrt(len(L))
    upper = numpy.mean(L) + 1.96*numpy.std(L)/math.sqrt(len(L))
    return (lower,upper)

## Model ----------
class Source(Process):
    """generate random arrivals"""
    def run(self, N, lamb, mu):
        for i in range(N):
            a = Arrival(str(i))
            activate(a, a.run(mu))
            t = random.expovariate(lamb)
            yield hold, self, t

class Arrival(Process):
    """an arrival"""
    n = 0  # class variable (number in system)

    def run(self, mu):
        # Event: arrival
        Arrival.n += 1   # number in system
        arrivetime = now()
        G.numbermon.observe(Arrival.n)

        
        if (Arrival.n>0):
            G.busymon.observe(1)
        else:
            G.busymon.observe(0)

        for p in range(G.K):
            if p != Arrival.n:
                G.m[p].observe(0)
        if(Arrival.n <G.K):
                G.m[Arrival.n].observe(1)

        # ... waiting in queue for server to be empty (delay) ...
        yield request, self, G.server
        t = random.expovariate(mu)
        yield hold, self, t
        yield release, self, G.server # let go of server (takes no simulation time)
        Arrival.n -= 1
        G.numbermon.observe(Arrival.n)
        delay = now()-arrivetime
        G.delaymon.observe(delay)#calculate wq
 

        for p in range(G.K):
            if p != Arrival.n:
                G.m[p].observe(0)
        if(Arrival.n <G.K):
                G.m[Arrival.n].observe(1)
                
        if (Arrival.n>0):
            G.busymon.observe(1)
        else:
            G.busymon.observe(0)



class G:
    server = 'dummy'
    delaymon = 'Monitor'
    numbermon = 'Monitor'
    busymon = 'Monitor'
    m= []#'Monitor list'
    K=10


def model(c, N, lamb, mu, maxtime, rvseed):
    # setup
    initialize()
    random.seed(rvseed)
    G.server = Resource(c, monitored = True)
    G.delaymon = Monitor()
    G.numbermon = Monitor()
    G.busymon = Monitor()#dont need
    
    G.m=[]
    i=0
    while i<G.K: 
        G.m.append( Monitor())
        i+=1
        
    # simulate
    s = Source('Source')
    activate(s, s.run(N, lamb, mu))
    simulate(until=maxtime)

    # gather performance measures
    W = G.delaymon.mean()
    L = G.numbermon.timeAverage()
    B = G.busymon.timeAverage()
 
    M=[]
    for j in range(G.K):
        M.append(G.m[j].timeAverage())
    Lq = G.server.waitMon.timeAverage()
    lambeff = L/W
    Wq = Lq/lambeff
    return(Wq,Lq,B, M)

## Experiment ----------------
K=10
allWQ = []
allLQ = []
allB = []
allLambdaEffective = []
allM = []

#for j in range(K):
#    allM.append([])

for k in range(50):
    seed = 123*k
    result = model(c=1, N=10000, lamb=2, mu=3,
                  maxtime=2000000, rvseed=seed)
    allWQ.append(result[0])
    allLQ.append(result[1])
    allB.append(result[2])
    allLambdaEffective.append(result[1]/result[0])
    allM.append(result[3])
 #   tempP = (result[3])
#    for j in range(K):
  #      allM[j].append(tempP[j])
#print allW
#print allL
#print allB
print ""
print "Estimate of Wq:",numpy.mean(allWQ)
print "Conf int of Wq:",conf(allWQ)
print "Estimate of Lq:",numpy.mean(allLQ)
print "Conf int of Lq:",conf(allLQ)
#print "Estimate of B:",numpy.mean(allB)
#print "Conf int of B:",conf(allB)
#print "Estimate of LambdaEffective:",numpy.mean(allLambdaEffective)
#print "Conf int of LambdaEffective:",conf(allLambdaEffective)
#print allM


for k in range (len(allM[G.K])):#each k
    resTemp =[]
    for row in range (len(allM)):#each row in allM
        resTemp.append(allM[row][k])
    print "Estimate of k=",k," : ",numpy.mean(resTemp)
    print "Conf int of k=",k,":",conf(resTemp)



   
#question 2

import matplotlib.pyplot as pl
x = numpy.linspace(-4,4,1000)
y =  (numpy.sin(numpy.pi*x))/(numpy.pi*x)

for i in range(len(x)):
    if x[i] ==0:
        y[i] =1

    
pl.clf()
pl.plot(x,y)
pl.title("$y = \sin{\pi*x}/{\pi*x}$", fontsize=16)
pl.xlabel("x", fontsize=16)
pl.ylabel("y", fontsize=16)
pl.axis("tight")
pl.savefig("myfig.png")
#pl.show()


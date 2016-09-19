#question1

from SimPy.Simulation import *
import random
import numpy
import math

def tablelookup(P):
    u = random.random()
    sumP =0.0
    for i in range(len(P)):
        sumP+=P[i]
        if u<sumP:
            return i

def conf(L):
    """confidence interval"""
    lower = numpy.mean(L) - 1.96*numpy.std(L)/math.sqrt(len(L))
    upper = numpy.mean(L) + 1.96*numpy.std(L)/math.sqrt(len(L))
    return (lower,upper)

## Model ----------
class Source(Process):
    """generate random arrivals"""
    num_arrivals = 0

    def run(self, N, lamb):
        for i in range(N):
            a = Arrival(str(i))
            activate(a, a.run())
            t = random.expovariate(lamb)
            yield hold, self, t


class Arrival(Process):
    """an arrival"""
    n = 0  # class variable (number in system)

    def run(self):
        Arrival.n += 1   # number in system
        arrivetime = now()
        G.numbermon.observe(Arrival.n)

        current = G.startnode
        while(current<>G.outnode):
            yield request,self,G.server[current]
            t = random.expovariate(G.mu[current])
            yield hold, self, t
            yield release, self, G.server[current]
            current = tablelookup(G.transition[current])

        Arrival.n -=1
        G.numbermon.observe(Arrival.n)
        delay = now()-arrivetime
        G.delaymon.observe(delay)

class G:
    server = 'dummy'
    delaymon = 'Monitor'
    numbermon = 'Monitor'
    startnode =0
    outnode = 3
    mu = [1/1.0,1/1.0,1/1.0]
    transition = [[0.0, 0.1, 0.9, 0.0],
                  [0.2, 0.0, 0.5, 0.3],
                  [0.0, 0.1, 0.0, 0.9]]

def model(N, lamb, maxtime, rvseed):
    #setup
    initialize()
    random.seed(rvseed)
    G.server = [Resource(2),Resource(2),Resource(2)]
    G.delaymon = Monitor()
    G.numbermon = Monitor()

    #simulate
    s = Source('Source')
    activate(s, s.run(N, lamb))
    simulate(until=maxtime)

    # gather performance measures
    W = G.delaymon.mean()
    L = G.numbermon.timeAverage()
    return (W,L)

             
## Experiment ----------------
allW = []
allL = []
for i in range(50):
    seed = 123*i
    result = model( N=10000, lamb=1.6,
                   maxtime=2000000, rvseed=seed)
    allW.append(result[0])
    allL.append(result[1])


print "Estimate of W:",numpy.mean(allW)
print "Conf int of W:",conf(allW)

print "Estimate of L:",numpy.mean(allL)
print "Conf int of L:",conf(allL)






    

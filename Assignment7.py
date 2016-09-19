
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
 #   n = 0  # class variable (number in system)

    def run(self, mu):
        # Event: arrival
        num_in_q = len(G.server.waitQ)
        if (num_in_q >=5):
            #print 'rej'
            G.rejectmon.observe(1)
            G.balkmon.observe(0)
            
        elif (random.random() <(0.2*num_in_q)):
            #balk
            G.balkmon.observe(1)
            G.rejectmon.observe(0)
        else:
            #print num_in_q
            G.rejectmon.observe(0)
            G.balkmon.observe(0)
#            Arrival.n += 1   # number in system
 #           arrivetime = now()

            yield request, self, G.server
            t = random.expovariate(mu)#check hours...
            yield hold, self, t
            yield release, self, G.server # let go of server (takes no simulation time)
            
            
            # Event: service ends
 #           Arrival.n -= 1

class G:
    server = 'dummy'
    balkmon = 'Monitor'
    rejectmon = 'Monitor'

def model(c, N, lamb, mu, maxtime, rvseed):
    # setup
    initialize()
    random.seed(rvseed)
    G.server = Resource(c)
    G.balkmon = Monitor()
    G.rejectmon = Monitor()
   
    # simulate
    s = Source('Source')
    activate(s, s.run(N, lamb, mu))
    simulate(until=maxtime)

    # gather performance measures
    Rej = G.rejectmon.mean()
    Pbalk = G.balkmon.mean()
    return(Rej,Pbalk)

## Experiment ----------------

Rej = []
Pbalk = []
for k in range(50):
    seed = 123*k
    result = model(c=1, N=10000, lamb=2.0, mu=2.0,
                   maxtime=2000000, rvseed=seed)
    Rej.append(result[0])
    Pbalk.append(result[1])
    
print "Estimate of Pbalk:",numpy.mean(Pbalk)
print "Conf int of Pbalk:",conf(Pbalk)
print "Estimate of Rejected:",numpy.mean(Rej)
print "Conf int of Rejected:",conf(Rej)












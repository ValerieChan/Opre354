#assignment 4

from SimPy.Simulation import *
import random

print "---Kathy (a)---"

## Model components-----------------------------
class Visitor(Process):
    """Visitor arrives at the mueseum and then leaves"""

    def visit(self, visitTime):
        arrive = now()
        print now(), self.name, "This is new"
        yield hold, self, visitTime
        print now(), self.name, "Nice Place!"
        print "Kathy - total time = ",now()-arrive
##Experiment data---------------------------------
MaxTime = 100
visitTime = 10

initialize()
K = Visitor(name = "Kathy")
activate(K, K.visit(visitTime), at=0)
simulate(until = MaxTime)


print "---Kathy (b)---"


## Model components-----------------------------
class VisitorB(Process):
    """Visitor arrives at the mueseum and then leaves"""

    def visitB(self, displayTime):
        i=0
        while i<len(displayTime):
            print now(), self.name, "Look!, number", i
            yield hold, self, displayTime[i]
            print now(), self.name, "mm"
            i+=1
        
##Experiment data---------------------------------
MaxTime = 100
visitTime = 10
displayTime = [4.5, 5.5]

initialize()
K = VisitorB(name = "Kathy")
activate(K, K.visitB(displayTime), at=0)
simulate(until = MaxTime)

print "---Kathy (c)---"


## Model components-----------------------------
class VisitorC(Process):
    """Visitor arrives at the mueseum and then leaves"""

    def visitC(self, displayTime):
        i=0
        print now(), self.name, "Look!, number", i
        yield hold, self, displayTime[i]
        random.seed(99999)
        j = random.random()
        #print j
        if(j <= 0.4):
            i = 1
        else:
            j=2
        print now(), self.name, "Look!, number", i
        yield hold, self, displayTime[i]
        print now(), self.name, "mm"
        
##Experiment data---------------------------------
MaxTime = 100
visitTime = 10
displayTime = [4.5, 5.5, 7.5]

initialize()
K = VisitorC(name = "Kathy")
activate(K, K.visitC(displayTime), at=0)
simulate(until = MaxTime)


print "---Kathy (d)---"


## Model components-----------------------------
class VisitorC(Process):
    """Visitor arrives at the mueseum and then leaves"""

    def visitC(self, displayTime):
        print now(), self.name, "Look!, number", 0
        
        random.seed(99999)
        j = 0
        while j<0.4:
            yield hold, self, displayTime
            print now(), self.name, "mm"
            j=random.random() 
        
        
        
##Experiment data---------------------------------
MaxTime = 100
visitTime = 10
displayTime = 4.5

initialize()
K = VisitorC(name = "Kathy")
activate(K, K.visitC(displayTime), at=0)
simulate(until = MaxTime)


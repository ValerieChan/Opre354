# Assignment 2

#1
import random
random.seed(123)
def gamble (n):
    i=0
    sucess =0
    while i<n:
        one = random.randint(1,6)#random no between 1-6
        two = random.randint(1,6)#random no between 1-6
        
        if (one is 6)  and (two is 6):
            #print"sucess"
            sucess = sucess+1
        i= i+1
    #print sucess
    #print n
    #print (sucess*1.0/n)
    if (sucess > 0):
        return 1
    return 0
def run(trials, gambles):
    print "The number of trials is:", trials
    i=0
    total = 0
    while i <trials:#set to 0 for now/....
        result =  gamble(gambles)
        #print result
        total = total +result
        i=i+1
    print total
    print "--------"

#A
#So in a trial of 10, 6 returned but 10 trials seems not enough to appear conclusive.
run(10,24)
#50 trials returned 23
run(50, 24)
#100 returned 50
run(100, 24)
#500 returned 261
run(500, 24)

#Seemingly you need more than 50 trials to get conclusively above 1/2.

print "---B---"

#B
# If the probability of a 6-6 needs to be "just" above 50% then if 100
#gambles are performed then:
run(100, 23)#returned 57
run(100, 24)#returned 55
run(100, 25)# returned 50
#25 appears to be optimal.


#2

import random


def tablelookup(y,p):
    """Sample from y[i] with probabilities p[i]"""
    u = random.random()
    sumP = 0.0
    for i in range(len(p)):
        sumP += p[i]
        if u < sumP:
            #print "i",i, "y[i]", y[i]
            return (y[i], i)


random.seed(123)

#i
y = [0,1,2,3,4,5]
p = [1.0/1024, 15.0/1024, 90.0/1024, 270.0/1024, 405.0/1024, 243.0/1024]
m = 1000000
valuetotal = 0.0
whole = {};

for k in range(m):
    d= tablelookup(y,p)
    whole[k]= d
    valuetotal += d[0]
print valuetotal/m

#for key, value in whole.items():
    #print value

# ii
y2 = [5,4,3,2,1,0]
p2 = [243.0/1024, 405.0/1024, 270.0/1024, 90.0/1024, 15.0/1024,  1.0/1024 ]
m2 = 1000000
valuetotal2 = 0.0
whole = {};

for k in range(m2):
    d= tablelookup(y2,p2)
    whole[k]= d
    valuetotal2 += d[0]
print valuetotal2/m2

# iii

y3 = [4,3, 5,2,1,0]
p3 = [405.0/1024,  270.0/1024, 243.0/1024,  90.0/1024, 15.0/1024,  1.0/1024 ]
m3 = 1000000
valuetotal3 = 0.0
whole = {};

for k in range(m3):
    d= tablelookup(y3,p3)
    whole[k]= d
    valuetotal3 += d[0]
print valuetotal3/m3


# The decending Y values of ii, have the fastest look up steps of 3.750114
# which is 0.000240 less average steps than option 1(3.750354). Option 3 was the
# slowest with average steps equalling 3.750704



#work for question 4
def pizzaPrice(state):
    if(state > 32.0):
        return 0
    PP=(16.0-(state/2.0))
    return PP

def pizzaDeath(state):
    m = ((state)/(10+pizzaPrice(state)))
    return m


def product(L):
    k=0
    i=0
    result = []
 
    while (k < 32):
        i=0
        x = 1
        while(i<k+1):
            x = L[i]* x
            i= i+1

        result.append(x)
        k=k+1
    return result

def PII():
    P3=[1]
    i=1
    while i<33:
        temp = P3[i-1]*c[i-1]
        P3.append(temp)
        i=i+1
    return P3
    

def Lam(biggest):
    List = []
    i=0
    while i< biggest:
        L = pizzaPrice(i)
        List.append(L)
        i=i+1
    List.append(0)#the last state where the price is 0...
    
    return List

def Mew(biggest):
    List = [0]
    i=1
    while i< biggest+1:
        L = pizzaDeath(i)
        List.append(L)
        i=i+1

    return List


print "---4.a---"

lamList = Lam(33)
mew = Mew(33)

c = []
i=0
while i<32:#calculating c
    c.append(lamList[i] / mew[i+1] )
    i=i+1
c.append(1)

#calculate the procuct of C (from 0 to 33)
productList= product(c)

#use other P calc
tempP = PII()

#normalise tempP
normalisation = sum(tempP)
finalP=[]
i=0
while i<32:
    finalP.append(tempP[i]/normalisation)
    i=i+1


#ex
temp2 = []
i=0
while i <32:
    temp2.append(i*finalP[i])
    i=i+1
finalEx = sum(temp2)

print "----output of vector list:----"
i=0
while i<32:#test print  
    print i,":::L",lamList[i], "M",mew[i], "C", c[i],"temp pi",tempP[i],"finalP",finalP[i]
    i=i+1

print "Po",finalP[0]
print "finalEx", finalEx


#Probability more than 20 is the sum of px more than 20.
print "---4.b---"
i=20
fraction =0
while i<32:
    fraction = fraction+  finalP[i]
    i=i+1
print "preportion of time",fraction





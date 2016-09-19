#Opre Assignent part 1

#1
#a

D = {'a':100}
D['b'] =200

#b
del D['b']

#c
L = [100]

L.append(200)

#d
L.remove(200)

#e
T = (100, 200, 300)

(a, b, c) = T


#2
#a
import random
import math
n=10
random.seed(123)
List=[]
i=0

while i <n:
    r = random.random()
    A = math.pi*(r**2)
    List.append((r, A))
    i = i+1

total_r=0
total_A=0

for item in List:
    print "r"
    print item[0]
    print "A"
    print item[1]
    total_r += item[0]
    total_A += item[1]

mean_r = total_r / n
mean_A = total_A /n

print "mean of r is: "
print mean_r
print "mean of A is : "
print mean_A

#c
n=100000
random.seed(123)
List=[]
i=0

while i <n:
    r = random.random()
    A = math.pi*(r**2)
    List.append((r, A))
    i = i+1

total_r=0
total_A=0

for item in List:
    total_r += item[0]
    total_A += item[1]

mean_r = total_r / n
mean_A = total_A /n

print "mean of r is: "
print mean_r
print "mean of A is : "
print mean_A

print "mean of pi*mean^2 is: "
print math.pi*(mean_r**2)


#The value of pi*(mean_r**2) is different
# to the  mean_A, because the distribution of
#individual r values when squared 'stretches more'
#than the averaged mean_r.

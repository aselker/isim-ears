#Find phase offset
import csv #for file import
from statsmodels.nonparametric.smoothers_lowess import lowess
import sys #for args
import os #for path join
import math #for sqrt, mostly
import matplotlib.pyplot as plt #for... wait, *something*...

freq = 366 #Hz
skipLines = 6 #Header lines
smoothLength = 7 #Must be odd if using medfilt -- unused
lowessFrac = 0.025 #Somthing to do with smoothing?
debug = True


def smooth(toSmooth, dist):
    smoothed = [0] * (len(toSmooth)-dist+1) #Overcomplicated empty list
    for i in range(len(toSmooth)-dist+1): #Iterate over the list, except fewer because we need a certain number of numbers to smooth properly
        smoothed[i] = sum (toSmooth[i:i+dist+1]) / dist
        #window = toSmooth[i:i+dist+1]
        
    return smoothed

def findPeaks(times, wave):
    mins = []
    maxs = []
    for i in range(1, len(wave)-1): #Don't iterate over the ends
        if (wave[i] > wave[i-1] and wave[i] > wave[i+1]):
            maxs.append((times[i], wave[i]))
            if(debug and False):
                print ("Found max at " + str(times[i]) + " with value " + str(wave[i]))
        elif (wave[i] < wave[i-1] and wave[i] < wave[i+1]):
            mins.append((times[i], wave[i]))
            if(debug and False):
                print ("Found min at " + str(times[i]) + " with value " + str(wave[i]))
        #elif debug:
        #    print ("Not a min or max, " + str(wave[i-1]) + " -> " + str(wave[i]) + " -> " + str(wave[i+1]) )

    return (mins, maxs)


def pointOffset(p1, p2):
    if len(p1) != len(p2):
        print ("List lengths are not equal.")
        return None
    else:
        return sum ([p2[i][0] - p1[i][0] for i in range(len(p1))]) / len(p1)

def approxOffset(p1, p2, dist):
    s = 0 #Offset sum
    count = 0
    for (x1, y1) in p1:
        for (x2, y2) in p2:
            if abs(x2 - x1) < dist: #If points are close enough
                s += (x2 - x1) #Add their separation to the offset list
                count += 1
    if count:
        return s / count
    else:
        print ("No pairs found.")
        return None
        

def findOffset(filename):
    
    rows=[]

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i in range(skipLines):
            next(reader) #skip some lines
        for row in reader:
            rows.append(row)


        times = []
        sig1 = []
        sig2 = []

        (times, sig1, sig2) = map(lambda x: map(float, x), zip(*rows)) #Unzip to get three lists
        times = list(times)
        
        sm1 = lowess(list(sig1), times, is_sorted=True, frac=lowessFrac, it=0)
        sm2 = lowess(list(sig2), times, is_sorted=True, frac=lowessFrac, it=0)
        
        (min1, max1) = findPeaks([x[0] for x in sm1], [x[1] for x in sm1])
        (min2, max2) = findPeaks([x[0] for x in sm2], [x[1] for x in sm2])
        
        offsetRange = ( #Set offset range based on average distance between peak points
            ( (min1[-1][0] - min1[0][0]) / len(min1) ) +
            ( (max1[-1][0] - max1[0][0]) / len(max1) ) +
            ( (min2[-1][0] - min2[0][0]) / len(min2) ) +
            ( (max2[-1][0] - max2[0][0]) / len(max2) )
        ) / 4
        
        return (approxOffset(min1, min2, offsetRange) + approxOffset(max1, max2, offsetRange) ) / 2

    
def offsetToPos(offset):
    l = 15.875 * 25.4 #mm
    y = 12 * 25.4 #mm
    speedOfSound = 343200 #mm/s

    d = offset * speedOfSound #Distance difference, mm

    #Math pulled mostly from Mathematica
    discriminant = d**6 - 2 * d**4 * l**2 + d**2 * l**4 - 4 * d**4 * y**2 + 4 * d**2 * l**2 * y**2

    sol1 = ( d**2 * l - l**3 - math.sqrt(discriminant) ) / ( 2 * (d ** 2 - l ** 2) )
    sol2 = ( d**2 * l - l**3 + math.sqrt(discriminant) ) / ( 2 * (d ** 2 - l ** 2) )

    if debug and False:
        print ("Solution 1: " + str(sol1 - 0.*l))
        print ("Solution 2: " + str(sol2 - 0.*l))

    return sol1


#print (offsetToPos(findOffset("Center.csv")))

pos = []
for i in range(0, 20, 2):
    csvName = os.path.join("csv", str(i) + "in.csv")
    offset = findOffset(csvName)
    if debug:
        print ("File " + csvName + ": Time offset = " + str(offset) )
    pos.append((i * 25.4,offsetToPos(offset)))

        
plt.plot ( [x[0] for x in pos], [x[1] for x in pos], 'b-')
plt.show()

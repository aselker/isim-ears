#Find phase offset
import csv #for file import
import matplotlib.pyplot as plt #for... wait, *something*...
import scipy.signal as signal
from statsmodels.nonparametric.smoothers_lowess import lowess

filename = "Center.csv"
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

def findPeaks(wave, times):
    mins = []
    maxs = []
    for i in range(1, len(wave)-1): #Don't iterate over the ends
        if (wave[i] > wave[i-1] and wave[i] > wave[i+1]):
            maxs.append((times[i], wave[i]))
            if(debug):
                print ("Found max at " + str(times[i]) + " with value " + str(wave[i]))
        elif (wave[i] < wave[i-1] and wave[i] < wave[i+1]):
            mins.append((times[i], wave[i]))
            if(debug):
                print ("Found min at " + str(times[i]) + " with value " + str(wave[i]))

    return (mins, maxs)
        

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

#sm1 = signal.medfilt(list(sig1), smoothLength) #Smooth the list
sm1 = lowess(list(sig1), times, is_sorted=True, frac=lowessFrac, it=0)
#sm1 = smooth (smooth( list(sig1), smoothLength), 5) #Double smoothing

(min1, max1) = findPeaks([x[0] for x in sm1], [x[1] for x in sm1])

plt.plot ( [x[0] for x in min1], [x[1] for x in min1], 'ro')
plt.plot ( [x[0] for x in max1], [x[1] for x in max1], 'bo')
plt.plot ( [x[0] for x in sm1], [x[1] for x in sm1], 'go')
plt.show ()

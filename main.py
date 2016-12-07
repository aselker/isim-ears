#Find phase offset
import csv #for file import

filename = "Center.csv"
freq = 366 #Hz
skipLines = 6 #Header lines
smoothLength = 100


def smooth(toSmooth, dist):
    smoothed = [0] * (len(toSmooth)-dist+1) #Overcomplicated empty list
    for i in range(len(toSmooth)-dist+1): #Iterate over the list, except fewer because we need a certain number of numbers to smooth properly
        smoothed[i] = sum (toSmooth[i:i+dist+1]) / dist
    return smoothed

def findPeaks(wave, times):
    mins = []
    maxs = []
    for i in range(1, len(wave)-1): #Don't iterate over the ends
        if (wave[i] > wave[i-1] and wave[i] > wave[i+1]):
            maxs.append(times[i])
        elif (wave[i] < wave[i-1] and wave[i] < wave[i+1]):
            mins.append(times[i])

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

sm1 = smooth(list(sig1), smoothLength) #Smooth the lists
sm2 = smooth(list(sig2), smoothLength)

(min1, max1) = findPeaks(sm1, list(times))

print (min1)

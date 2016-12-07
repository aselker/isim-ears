#Find phase offset
import csv #for file import

filename = "Center.csv"
freq = 366 #Hz
skipLines = 6 #Header lines
smoothLength = 100


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



def smooth(toSmooth, dist):
    smoothed = [0] * (len(toSmooth)-dist+1)
    for i in range(len(toSmooth)-dist+1):
        smoothed[i] = sum (toSmooth[i:i+dist+1]) / dist
    return smoothed

sm1 = smooth(list(sig1), smoothLength)
sm2 = smooth(list(sig2), smoothLength)


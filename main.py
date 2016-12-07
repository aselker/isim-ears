#Find phase offset
import csv #for file import

filename = "main.csv"
freq = 366 #Hz

with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        print (', '.join(row))

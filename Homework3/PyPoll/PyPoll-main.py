#Import 
import os
import csv

#read CSV file
csvpath = os.path.join('Resources','election_data.csv')

with open(csvpath, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')

print(csvreader)

for row in csvreader:
    print(row)

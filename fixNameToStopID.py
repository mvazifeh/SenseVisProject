'''
Created on Mar 29, 2015

@author: Hongmou
'''
import csv

nameToStop = 'C:/Users/Hongmou/Desktop/stopNames.csv'
stopNameDict = dict()
ct = 0

dup = list()
with open(nameToStop, 'rb') as f:
    rd = csv.reader(f)
    row = rd.next()
    nameId = row.index('STOP_NAME')
    stopIdId = row.index('STOP_ID')
    for row in rd:
        if row[nameId] not in stopNameDict:
            stopNameDict[row[nameId]] = row[stopIdId]
        else:
            print 'duplicate: ' + row[nameId]
            dup.append(int(row[0]))
            ct += 1

print ct
print dup

# Too many duplicate names with different locations
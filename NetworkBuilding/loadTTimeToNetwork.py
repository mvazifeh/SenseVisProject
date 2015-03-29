'''
Created on Mar 29, 2015

@author: Hongmou
'''

import cPickle
import csv

ttime = 'C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Data/Bus/Processed_data_mohammad/transit_times_network_24_2'
f = open(ttime, 'rb')
nd = cPickle.load(f) # travel time dictionary
f.close()

unseen = list()

bus_segment = 'C:/Users/Hongmou/Desktop/bus_segment.csv'
with open(bus_segment, 'rb') as g:
    rd = csv.reader(g)
    row = rd.next()
    stId1 = row.index('STOP_ID')
    stId2 = row.index('STOP_ID_1')
    for row in rd:
        stPair = ('"{}"'.format(row[stId1]), '"{}"'.format(row[stId2]))
        if stPair not in nd:
            if stPair not in unseen:
                unseen.append(stPair)

print len(unseen)

for stp in unseen:
    print stp
    
unusedSt = {'"31246"', '"18332"', '"30884"', '"49701"', '"14000"', '"192"', '"28740"', '"4424"', '"11081"', '"11082"', '"11083"', '"11085"', '"11086"', '"3537"', '"11091"', '"11092"', '"11094"', '"11095"', '"11096"', '"11097"', '"30885"', '"12001"', '"12002"', '"12003"', '"12004"', '"11240"', '"1389"', '"3059"', '"6261"', '"6266"', '"6270"'}


notBecauseUnused = list()
for i in unseen:
    if i[0] not in unusedSt and i[1] not in unusedSt:
        notBecauseUnused.append(i)
        
print "===========================" + str(len(notBecauseUnused)) + "==========================="
for i in notBecauseUnused:
    print i

segment_unknown_id = list()
bus_segment = 'C:/Users/Hongmou/Desktop/bus_segment.csv'
with open(bus_segment, 'rb') as g:
    rd = csv.reader(g)
    row = rd.next()
    stId1 = row.index('STOP_ID')
    stId2 = row.index('STOP_ID_1')
    oid = 0
    for row in rd:
        stPair = ('"{}"'.format(row[stId1]), '"{}"'.format(row[stId2]))
        if stPair in notBecauseUnused:
            segment_unknown_id.append(int(row[oid]))

print segment_unknown_id 
            
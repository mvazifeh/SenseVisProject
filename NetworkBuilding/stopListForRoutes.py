'''
Created on Mar 19, 2015

@author: Hongmou
'''
import csv

rtList = dict()

# rtList gives the sequence of stations for each route (branches and directions)
with open('C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Data/Bus/StopListForRoute/StopLists.csv', 'rb') as f: # subject to change
    rd = csv.reader(f)
    row = rd.next()
    rtId = row.index('CTPS_ROU_1')
    frStId = row.index('FROM_STOP_')
    toStId = row.index('TO_STOP_ID')
    for row in rd:
        rt = row[rtId]
        if rt in rtList:
            curLen = len(rtList[rt])
            if rtList[rt][curLen - 1] == row[frStId]:
                rtList[rt].append(row[toStId])
            else:
                print str(rt) + ': error'
        else:
            rtList[rt] = [row[frStId], row[toStId]]

# You can add your own output methods here
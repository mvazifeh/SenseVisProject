'''
Created on Mar 25, 2015

@author: Hongmou
@summary: This py is for listing the coordinates of stops for each route
'''
import csv

stopListTable = 'C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Data/Bus/StopListForRoute/routeStopCount_HM.csv'
stopCoordTable = 'C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Data/Bus/StopListForRoute/StopCoords.csv'
outputFile = 'C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Data/Bus/StopListForRoute/routeStopCoords.csv'

# Read coordinates into a dictionary
coordDict = dict()
with open(stopCoordTable, 'rb') as f:
    rd = csv.reader(f)
    row = rd.next()
    stopId = row.index('STOP_ID')
    latId = row.index('lat')
    lonId = row.index('lon')
    for row in rd:
        coordDict[row[stopId]] = (float(row[latId]), float(row[lonId]))

# For each route, get the stop list and look up for the coordinates in the stop list dictionary
with open(outputFile, 'wb') as g:
    wt = csv.writer(g)
    with open(stopListTable, 'rb') as f:
        rd = csv.reader(f)
        row = rd.next()
        routeId = row.index('ROUTE_ID')
        stopListId = row.index('STOP_LIST')
        for row in rd:
            stopStr = row[stopListId].replace('\'', '')
            stopList = stopStr[1:len(stopStr) - 1].split(', ')
            coordList = list()
            for stop in stopList:
                if stop in coordDict:
                    coordList.append(coordDict[stop])
                else:
                    print 'Not found!'
            wt.writerow([row[routeId], coordList])
            
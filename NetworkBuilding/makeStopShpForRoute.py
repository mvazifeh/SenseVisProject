'''
Created on Mar 24, 2015
@author: Hongmou
@summary: This py splits the stop shapefile for each bus route
'''

import arcpy, csv

stopShapefile = 'C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Shapefiles/Bus/MBTABUSSTOPS_PT.shp'
routeShapefile = 'C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Shapefiles/Bus/MBTABUSROUTES_ARC.shp'
stopListTable = 'C:/Users/Hongmou/Dropbox (MIT)/HubCity_Hack/Data/Bus/StopListForRoute/routeStopCount_HM.csv'
outputFolder = 'C:/Projects/MassHackathon/stopsForRoutes/'

# CAUTION: may overwrite the current shapefiles in the output folder
arcpy.env.overwriteOutput = True


routeList = list()
with open(stopListTable, 'rb') as f:
    rd = csv.reader(f)
    row = rd.next()
    routeId = row.index('ROUTE_ID')
    stopListId = row.index('STOP_LIST')
    # Add all bus stops to a Layer
    arcpy.MakeFeatureLayer_management(stopShapefile, 'stopLayer')
    # Add all routes to a layer
    arcpy.MakeFeatureLayer_management(routeShapefile, 'routeLayer')
    # For each route
    for row in rd:
        stopListStr = row[stopListId]
        stopList = stopListStr.replace('\'', '').replace('[','(').replace(']',')')
        # Select the stops of this route from the stop layer
        arcpy.SelectLayerByAttribute_management('stopLayer', 'NEW_SELECTION', 'STOP_ID IN '+ stopList)
        # Export the selection to a new shapefile
        arcpy.CopyFeatures_management("stopLayer", outputFolder + 'routePt' + row[routeId])
        # Select the route from the route layer
        arcpy.SelectLayerByAttribute_management('routeLayer', 'NEW_SELECTION', 'CTPS_ROU_2 = '+ row[routeId])
        # Export the route to a new shapefile
        arcpy.CopyFeatures_management("routeLayer", outputFolder + 'routeAc' + row[routeId])
        # Add the route to the list
        routeList.append(row[routeId])


# Split each route with its stops
toBeMerged = list()
for rt in routeList:
    lineFile = outputFolder + 'routeAc' + rt + '.shp'
    pointFile = outputFolder + 'routePt' + rt + '.shp'
    outputFile = outputFolder + 'routeSplit/' + 'split' + rt + '.shp'
    arcpy.SplitLineAtPoint_management(lineFile, pointFile, outputFile, '0.5 Meters')
    toBeMerged.append(outputFile)
    
# Merge all split segment into one shapefile
arcpy.Merge_management(toBeMerged, outputFolder + 'routeSplit/' + 'splitBusRoutes.shp')
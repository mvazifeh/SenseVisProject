import qgis
from qgis.core import *
qgis.utils.iface
from qgis.utils import iface
from PyQt4.QtCore import QVariant

lyrs = iface.legendInterface().layers()
buffers = lyrs[1]
Bus_points = lyrs[0]

Buffer_feature = buffers.getFeatures() #get all features of poly layer

# Method 1

for Buffer_feature in Buffer_features: #iterate poly features
    stopID = Buffer_feature["STOP_ID"] #get attribute of poly layer
    geomBuffer = Buffer_feature.geometry() #get geometry of poly layer
    
    #performance boost: get point features by poly bounding box first
    point_feature = Bus_points.getFeatures(QgsFeatureRequest().setFilterRect(geomPoly.boundingBox()))
    for point_feature in point_features:
        
        #iterate preselected point features and perform exact check with current polygon
        if point_feature.geometry().within(geomBuffer):
            print '"' + stopID + '"' + ';' + point_feature["STOP_ID"]
            
            


# Method 2 - 

while provider.nextBuffer_feature(Buffer_feature):
    if (Buffer_feature.geometry().contains(QgsGeometry.fromBus_points(QgsPoint(lLON, LAT)))): # must change field names in attribute table (LAT, LON)!
        print 'Contained in feature %d' % feature.id()
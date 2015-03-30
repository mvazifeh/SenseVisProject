'''
Created on Mar 23, 2015

@author: mmvazifeh
'''
import shapefile
from os.path import expanduser

folder_add = expanduser('~/Dropbox/HubCity_Hack/Shapefiles/Bus/constant_polygons/tt0/')
filename = 'tt0_ObjectID__1.shp'
# # read the shapefile
# list = [[1,5],[5,5],[5,1],[3,3],[1,1]]
# for i in list:
#     w = shapefile.Writer(shapefile.POLYGON)
#     w.poly(parts=[list])
#     w.field('F_FLD','C','40')
#     w.field('S_FLD','C','40')
#     w.record('First','Polygon')
#     w.save('Shape.shp')

# read the shapefile
reader = shapefile.Reader(folder_add+filename)
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", \
     geometry=geom, properties=atr)) 

# write the GeoJSON file
from json import dumps
geojson = open(folder_add +filename[:-4] + '.json', "w")
geojson.write(dumps({"type": "FeatureCollection",\
 "features": buffer}, indent=2) + "\n")
geojson.close()

'''
Created on Mar 27, 2015

@author: Hongmou
'''
import arcpy

field_names = ['FID','Shape','SHAPE_ID','MBTA_ROUTE','MBTA_VARIA','MBTA_ROU_1','CTPS_ROUTE','CTPS_ROU_1','DIRECTION','ROUTE_DESC','TRIP_HEADS','CTPS_ROU_2','SHAPE_Leng','FID_1','Join_Count','dist1','TARGET_FID','SHAPE_ID_1','MBTA_ROU_2','MBTA_VAR_1','MBTA_ROU_3','CTPS_ROU_3','CTPS_ROU_4','DIRECTIO_1','ROUTE_DE_1','TRIP_HEA_1','CTPS_ROU_5','SHAPE_Le_1','ORIG_FID','STOP_ID','STOP_NAME','TOWN','TOWN_ID','FID_12','Join_Cou_1','dist2','TARGET_F_1','SHAPE_ID_2','MBTA_ROU_4','MBTA_VAR_2','MBTA_ROU_5','CTPS_ROU_6','CTPS_ROU_7','DIRECTIO_2','ROUTE_DE_2','TRIP_HEA_2','CTPS_ROU_8','SHAPE_Le_2','ORIG_FID_1','STOP_ID_1','STOP_NAM_1','TOWN_1','TOWN_ID_1','Shape_Length']

arcpy.env.workspace = 'C:/Projects/MassHackathon/stopsForRoutes/splitRoute.gdb'

featureclasses = arcpy.ListFeatureClasses()

for fc in featureclasses:
    field_list = arcpy.ListFields(fc)
    for i in range(len(field_list)):
        if i > 1 and i != 53:
            arcpy.AlterField_management(fc, field_list[i].name, field_names[i])
        
arcpy.Merge_management(featureclasses, 'mergeSplit')
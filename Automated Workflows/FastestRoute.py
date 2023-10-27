import arcpy
from pprint import pprint
import os

# Declare variables
naxName = "Fastest Route"
inputCoords = [[-8992565.9786, 4177515.069799997],[-9002133.2243, 4192345.9389000013]]
gdb = r"C:\Users\tim10393\Documents\ArcGIS\Projects\NetworkAnalysis\Default.gdb"
inBarFcName = "Barriers"
inStopFcName = "StopsFc" 
inStopFc = os.path.join(gdb, inStopFcName)

arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

#Create a table
arcpy.management.CreateFeatureclass(out_path=gdb, out_name=inStopFcName, geometry_type="Point", spatial_reference=3857)

# Provide input stop data for the insert cursor
cur = arcpy.da.InsertCursor(inStopFcName, ["Shape@"])
for coord in inputCoords:
    pnt = arcpy.Point(coord[0],coord[1])
    pntGeom = arcpy.PointGeometry(pnt)
    cur.insertRow([pntGeom])
del cur

#Create the analysis layer
naxLyr = arcpy.na.MakeRouteAnalysisLayer(
    network_data_source="https://www.arcgis.com/",
    layer_name=naxName)
print("Network analysis layer created")

# Add the stop locations
arcpy.na.AddLocations(
    in_network_analysis_layer=naxLyr,
    sub_layer="Stops",
    in_table=inStopFc)
print("Input locations added")

# Add the barriers
arcpy.na.AddLocations(
    in_network_analysis_layer=naxLyr,
    sub_layer="Polygon Barriers",
    in_table=inBarFcName)
print("Barriers added")

# Solve the problem
arcpy.na.Solve(
    in_network_analysis_layer=naxLyr)
print("Problem solved")

arcpy.management.Delete(inStopFc)

pprint(arcpy.da.Describe(naxLyr[0]))
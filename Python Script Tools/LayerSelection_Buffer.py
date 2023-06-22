import arcpy
arcpy.env.overwriteOutput = True
inFeatures = arcpy.GetParameterAsText(0)
exp = arcpy.GetParameterAsText(1)
outBuff = arcpy.GetParameterAsText(2)
sp = arcpy.GetParameter(3)

gasStatLyr = arcpy.management.SelectLayerByAttribute(in_layer_or_view = inFeatures, where_clause= exp)

#sp = arcpy.Describe(inFeatures).spatialReference

count = arcpy.GetCount_management(gasStatLyr)
if count == 0:
    arcpy.AddMessage("There are not features from the selection.")
else:
    arcpy.AddMessage(f"There are {count} features from the selection.")
# This creates a buffer
arcpy.env.outputCoordinateSystem = sp
arcpy.analysis.Buffer(gasStatLyr, outBuff, "0.75 Miles", method="GEODESIC")




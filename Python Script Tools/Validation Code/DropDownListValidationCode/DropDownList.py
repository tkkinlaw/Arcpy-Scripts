import arcpy

arcpy.env.overwriteOutput = True

planning_gisowner_streams = arcpy.GetParameterAsText(0)
field = arcpy.GetParameter(1)
value = arcpy.GetParameterAsText(2)
outputFilePath = arcpy.GetParameterAsText(3)

#planning_gisowner_streams = r"C:\Users\tim10393\OneDrive - Esri\DemoData\DemoData.gdb\LinvilleGorgeTrail"
#field = 'unittype'
#value = "Name"
#outputFilePath = r"C:\Users\tim10393\OneDrive - Esri\DemoData\DemoData.gdb\deleteMe"

Expression = "{} = '{}'".format(field, value)

streamSelection = arcpy.management.SelectLayerByAttribute(in_layer_or_view=planning_gisowner_streams, where_clause=Expression)

arcpy.analysis.Buffer(in_features = streamSelection, out_feature_class = outputFilePath, buffer_distance_or_field = "100 Feet")
arcpy.AddMessage("All done")
print("Done")
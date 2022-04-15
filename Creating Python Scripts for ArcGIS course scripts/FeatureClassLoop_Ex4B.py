import arcpy

# Set the workspaces
arcpy.env.workspace = r"C:\EsriTraining\PYTS\Data\CountyData.gdb"
outWorkspace = r"C:\EsriTraining\PYTS\Default.gdb"
fcList = arcpy.ListFeatureClasses("", "Point")
for fc in fcList:
    outputFC = "{}\\{}".format(outWorkspace, fc)
    arcpy.CopyFeatures_management(fc, outputFC)
    print("{} copied".format(fc))

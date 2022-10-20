import arcpy

# Set the workspaces
arcpy.env.workspace = r"C:\EsriTraining\PYTS\Data\CountyData.gdb"
outWorkspace = r"C:\EsriTraining\PYTS\Default.gdb"
fcList = arcpy.ListFeatureClasses("", "Point")
for fc in fcList:
    outputFC = f"{outWorkspace}\\{fc}"
    arcpy.CopyFeatures_management(fc, outputFC)
    print(f"{fc} copied")

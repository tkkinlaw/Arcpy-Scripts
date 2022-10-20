arcpy.env.workspace = r"C:\EsriTraining\PYTS\Data"
gdbList = arcpy.ListWorkspaces("", "FileGDB")
print(gdbList)
arcpy.env.workspace = r"C:\EsriTraining\PYTS\Data\CountyData.gdb"
fcList = arcpy.ListFeatureClasses()
print(fcList)
fcList2 = arcpy.ListFeatureClasses("", "Point")
print(fcList2)
fieldList = arcpy.ListFields('ParcelPts')
print(fieldList[8].name)

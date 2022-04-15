import arcpy

arcpy.env.workspace = r"C:\Demos\PYTS\SANDAG\Ecology"
gdbLoc = r"C:\Demos\PYTS\SanDiego.gdb"

fcList = arcpy.ListFeatureClasses()

print(fcList)

fcNum = len(fcList)
try:
    for fc in fcList:
        print(fc)
        newName = fc.replace(".shp","")

        arcpy.FeatureClassToFeatureClass_conversion(fc,gdbLoc) #Removed the , newName in the GP Tool, causing it to fail
except arcpy.ExecuteError:
    print(arcpy.GetMessages())


import arcpy 
import os

arcpy.env.workspace = r"C:\Users\student\Desktop\PYTS\SANDAG\Ecology"
listShapefile = arcpy.ListFeatureClasses()
print(listShapefile)

outputGDB = r"C:\Users\student\Desktop\PYTS\Testing.gdb"
for shp in listShapefile:
    print(shp)
    newName = os.path.join(outputGDB, shp.replace(".shp", ""))
    print(newName)
    desc = arcpy.Describe(shp)
    if desc.shapeType == "Point":
        inputData = os.path.join(r"C:\Users\student\Desktop\PYTS\SANDAG\Ecology", shp)
        arcpy.analysis.Buffer(inputData, newName, "500 Meters")
        print(shp)
    else:
        print("It's not a point!!")
print("All done.")
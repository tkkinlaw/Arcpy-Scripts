# We have a folder of Shapefiles: C:\Users\student\Desktop\PYTS\SANDAG\Ecology
# We want to run the buffer tool on each, if it is Polygon geometry.
# The outputs should live in a new geodatabase: C:\Users\student\Desktop\PYTS\SANDAG\Ecology.gdb

import arcpy
import os
import time
startTime = time.time()
# This will be the input location for where the shapefiles are
baseFolder = r'C:\Users\student\Desktop\PYTS\SANDAG'

arcpy.env.workspace = os.path.join(baseFolder, "Ecology")

# Specify the output geodatabase and create it
arcpy.management.CreateFileGDB(out_folder_path=baseFolder, out_name="Ecology.gdb")
outGDB = r"C:\Users\student\Desktop\PYTS\SANDAG\Ecology.gdb"
# List the shapefiles
shpList = arcpy.ListFeatureClasses(feature_type="Polygon")

for shp in shpList:
    print(shp)
    newName = shp.split('.shp')[0]
    outFC = f"{outGDB}\\{newName}"
    if arcpy.Exists(outFC):
        print(f'{outFC} exists')
    else:
        print(f"{outFC} does not exists")
        arcpy.analysis.Buffer(shp, outFC, "1 Mile")
        print(f"{outFC} buffer created")

print(shpList)
endTime = time.time()
print(f"The process took: {round(endTime-startTime, 3)} seconds")
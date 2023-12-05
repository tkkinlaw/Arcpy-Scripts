# We have a folder of Shapefiles: C:\Users\student\Desktop\PYTS\SANDAG\Ecology
# We want to run the buffer tool on each, if it is Polygon geometry.
# The outputs should live in a new geodatabase: C:\Users\student\Desktop\PYTS\SANDAG\Ecology.gdb
# 1 Mile

# Step 1 - import packages
import arcpy, os

# Step 2 - set workspace & create variables
shpFolder = r"C:\Users\student\Desktop\PYTS\SANDAG\Ecology"
buffGDB = r"C:\Users\student\Desktop\PYTS\SANDAG\Ecology.gdb"
arcpy.env.workspace = shpFolder

# Step 3 - create the output geodatabase
gdbPathParts = os.path.split(buffGDB)
gdbPath = gdbPathParts[0]
gdbName = gdbPathParts[1]
if arcpy.Exists(buffGDB):
    print(f"{buffGDB} already exists")
    pass
else:
    arcpy.CreateFileGDB_management(out_folder_path=gdbPath, out_name=gdbName)
    print(f"{gdbName} has been created at {gdbPath}")

# Step 4 - get list of feature classes
shpList = arcpy.ListFeatureClasses()
print(shpList)

# Step 5 - Create the For-Loop, identify the Polygons, and then run the buffer
for shp in shpList:
    # Use Describe to identify is SHP is a Polygon shapeType
    d = arcpy.da.Describe(shp)
    if d['shapeType'] == "Polygon":
        print(f"{shp} is a polygon geometry type. Running the buffer tool.")
        # Run the buffer tool on the polygon shapefile.
        outBuffPath = os.path.join(buffGDB, d['baseName']) #f"{buffGDB}\\{d['baseName']}Buffer"
        arcpy.analysis.Buffer(in_features=shp, out_feature_class=outBuffPath, buffer_distance_or_field='1 Mile')
print("All done.")
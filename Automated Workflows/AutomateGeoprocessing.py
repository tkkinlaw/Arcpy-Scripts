# We have a folder of Shapefiles: C:\Users\student\Desktop\PYTS\SANDAG\Ecology
# We want to run the buffer tool on each, if it is Polygon geometry.
# The outputs should live in a new geodatabase: C:\Users\student\Desktop\PYTS\SANDAG\Ecology.gdb
# 1 Mile

# Step 1: import packages
import arcpy, os

# Step 2: Define variables
shpFolder = r"C:\Users\student\Desktop\PYTS\SANDAG\Ecology"
newGDBLoc = r"C:\Users\student\Desktop\PYTS\SANDAG"
newGDBName = "Ecology.gdb"
newGDBPath = os.path.join(newGDBLoc, newGDBName)
# Step 3: set the workspace
arcpy.env.workspace = shpFolder

# Step 4: Create output geodatabase arcpy.management.CreateFileGDB(out_folder_path, out_name, {out_version})
if arcpy.Exists(newGDBPath):
    print("The geodatabase exists")
else:
    print("Creating a new geodatabase")
    arcpy.management.CreateFileGDB(out_folder_path=newGDBLoc, out_name=newGDBName)

# Step 5: Get the polygon features
shpList = arcpy.ListFeatureClasses(None, "Polygon")
print(shpList)

# Step 6: Execute the buffer tool
for polygon in shpList:
    print(polygon)
    # create a variable that represents the full file path of the output
    desc = arcpy.Describe(polygon)
    outBuff = os.path.join(newGDBPath, desc.baseName)
    # Run the buffer tool
    arcpy.analysis.Buffer(in_features=polygon, out_feature_class=outBuff, buffer_distance_or_field="1 Mile")
    print(f"{polygon} buffer created")
print("All done")
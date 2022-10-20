# import site package
import arcpy

# Access describe object
desc = arcpy.Describe(r'C:\EsriTraining\PYTS\Data\CountyData.gdb\ParcelPts')
# Variable for properties
dPath = desc.path
print(dPath)
dName = desc.baseName
dGeometry = desc.shapeType
dCoord = desc.spatialReference
# Modify output feature
newName = f"{dName}_new"
print(newName)
# Create new feature class
arcpy.CreateFeatureclass_management(dPath, newName, dGeometry, None, "", "", dCoord)
print("Script Complete")
# import modules
import arcpy
import csv

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(103501)
print("Modules imported and environments set.")

# variables
outageXY = r"C:\EsriTraining\PYTS\Data\OutageXY.csv"
outConvexHull = r"C:\EsriTraining\PYTS\Data\Outages.gdb\CurrentAffectedArea"
outputJoin = r"in_memory\outputJoin"
serviceAreas = r"C:\EsriTraining\PYTS\Data\CountyData.gdb\ServiceAreas"
print("Variables are set.")

# Append coordinates from csv in a list
outageCoords = []
csvFile = open(outageXY)
csvReader = csv.reader(csvFile)
next(csvReader)
for row in csvReader:
    outageCoords.append(row)

# Create a multipoint geometry object from list of coordinates
pntLst = []
for coords in outageCoords:
    pnt = arcpy.Point(coords[0], coords[1])
    pntLst.append(pnt)
pntAry = arcpy.Array(pntLst)
outagePoints = arcpy.Multipoint(pntAry)
print("Geometry object created")

# Create outage boundary using convex hull
convexHull = outagePoints.convexHull()
arcpy.CopyFeatures_management(convexHull, outConvexHull)
print("Outage boundary created")

# Use Spatial Join to identify affected areas
arcpy.SpatialJoin_analysis(serviceAreas, outagePoints, outputJoin)
print("Spatial join finished.")

# Search join output
sFields = ['Join_Count', 'ServArNu']
exp = '"Join_Count" = 1'
print("Affected service areas")
with arcpy.da.SearchCursor(outputJoin, sFields, exp) as sCursor:
    for row in sCursor:
        print(f"Service Area: {row[1]}")
del sCursor

print("Analysis complete.")

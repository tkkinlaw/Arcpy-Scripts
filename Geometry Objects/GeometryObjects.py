import arcpy
import csv
import numpy

# Read coordinates from a csv and create a Polyline geometry object
file = r"C:\DemoData\PYTS\BlueSkyEcologicalStream.csv"
csvFile = open(file)
csvReader = csv.reader(csvFile)

pnt = arcpy.Point()
ary = arcpy.Array()

for row in csvReader:
    pnt.X = row[0]
    pnt.Y = row[1]
    ary.append(pnt)

streamGeom = arcpy.Polyline(ary)

# Use a geometry object method to determine sample point locations
samplePerc = numpy.arange(.25,1.25,.25)
for perc in samplePerc:
    samplePoint = streamGeom.positionAlongLine(perc,True)
    print("{} sample point is at the following location x:{} y:{}".format(perc, samplePoint.centroid.X,
                                                                          samplePoint.centroid.Y))

# Create an empty feature class
arcpy.CreateFeatureclass_management("C:\DemoData\PYTS\SanDiego.gdb","StreamSamplePts", "Point", spatial_reference=2230)

# Use insert cursor to add points to feature class
cursor = arcpy.da.InsertCursor("C:\DemoData\PYTS\SanDiego.gdb\StreamSamplePts","Shape@XY")

for perc in samplePerc:
    samplePoint = streamGeom.positionAlongLine(perc, True)
    cursor.insertRow([(samplePoint.centroid.X, samplePoint.centroid.Y)])

del cursor

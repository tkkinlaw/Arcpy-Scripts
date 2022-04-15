####################################################################
# Name: PowerOutage.py
# Description: Power outage Python script for use with script tool
# Author: Esri Training
# Course: PYTS
####################################################################

# import modules
import arcpy
import csv
import sys

# create custom exception classes for error handling


class PhoneEmptyRows(Exception):
    pass


class XyEmptyRows(Exception):
    pass


# set environments
arcpy.env.workspace = r"C:\EsriTraining\PYTS\Data"
arcpy.env.overwriteOutput = True

# set parameters for input/output files
# input outage files
pNumFile = arcpy.GetParameterAsText(0)
# r"C:\EsriTraining\PYTS\Data\PhoneReports.csv"
xyFile = arcpy.GetParameterAsText(1)
# r"C:\EsriTraining\PYTS\Data\SocialMediaReports.xlsx\SocialMediaXY$"
ptFile = arcpy.GetParameterAsText(2)
# r"C:\EsriTraining\PYTS\Data\AppReports.shp"
parcelPoints = r"C:\EsriTraining\PYTS\Data\CountyData.gdb\Parcelpts"
serviceAreas = r"C:\EsriTraining\PYTS\Data\CountyData.gdb\ServiceAreas"
outputGDB = r"C:\EsriTraining\PYTS\Data\Outages.gdb"


# Derived from input parameters
serviceAreasJoin = "in_memory\\join"
# outages = "{0}\Outages".format(outputGDB)
# outageDensity = "{0}\OutageDensity".format(outputGDB)
# outConvexHull = "{0}\OutageArea".format(outputGDB)
outages = outputGDB + "\\Outages"
outageDensity = outputGDB + "\\OutageDensity"
outConvexHull = outputGDB + "\\OutageArea"

# error handling
try:
    # import app point shapefile into file geodatabase
    print ("Importing app points into Outage FC")
    arcpy.AddMessage("Importing app points into Outage FC")
    arcpy.FeatureClassToFeatureClass_conversion(ptFile, outputGDB, 'Outages')
    # create point file from social media excel spreadsheet and append to outages feature class
    print("Creating pointFC from social media table")
    arcpy.AddMessage("Creating pointFC from social media table")

    # get count of rows in XY file for error handling
    xyCount = arcpy.GetCount_management(xyFile)
    if int(xyCount[0]) > 0:
        xyEvent = "XY_Event_Layer"
        spatialRef = arcpy.SpatialReference(103501)
        arcpy.MakeXYEventLayer_management(xyFile, "Point_X", "Point_Y", xyEvent, spatialRef)
        arcpy.Append_management(xyEvent, outages, "NO_TEST")
    else:
        # Raise exception
        raise PhoneEmptyRows(xyCount)

    # from phone number csv look up number in parcel points feature class using search cursor.
    # pull shapeXY geometry and add to a list
    print("Looking up phone numbers")
    arcpy.AddMessage("Looking up phone numbers")
    # get count of rows in CSV for error handling
    pNumCount = arcpy.GetCount_management(pNumFile)
    arcpy.AddMessage("{} phone numbers".format(pNumCount))
    if int(pNumCount[0]) > 0:
        pList = []
        csvFile = open(pNumFile)
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            with arcpy.da.SearchCursor(parcelPoints, ['Phone_Number', 'SHAPE@XY']) as sCursor:
                for sRow in sCursor:
                    if row[0] == sRow[0]:
                        pList.append(sRow[1])
            del sCursor
    else:
        # Raise exception
        raise XyEmptyRows(pNumCount)

    # insert shapexy geometry from list into outages feature class  'PhoneNum_1'
    print("Inserting phone number points into outage FC")
    arcpy.AddMessage("Inserting phone number points into outage FC")
    iCursor = arcpy.da.InsertCursor(outages, ['SHAPE@X', 'SHAPE@Y'])
    for pRow in pList:
        iCursor.insertRow(pRow)
    del iCursor

    # create kernel density map

    print("Creating Kernel density")
    arcpy.AddMessage("Creating Kernel density")
    arcpy.env.extent = arcpy.Extent(2053764.41650888, 507185.366399556, 2115439.05332997, 551798.058013887)
    populationField = "NONE"
    cellSize = 100
    searchRadius = ""
    outKernelDensity = arcpy.sa.KernelDensity(outages, populationField, cellSize, searchRadius, "SQUARE_MILES")
    outKernelDensity.save(outageDensity)

    # create convex hull
    # create multipoint feature class from points
    print("Creating convex hull")
    arcpy.AddMessage("Creating convex hull")
    multipoints = arcpy.Dissolve_management(in_features=outages,
                                            out_feature_class=r"in_memory\multi",
                                            dissolve_field=None,
                                            multi_part=True)
    points = [f[0].convexHull() for f in arcpy.da.SearchCursor(multipoints, "SHAPE@")]
    arcpy.CopyFeatures_management(points, outConvexHull)

    # Determine which service areas need to be sent
    print("Joining outage points with service area")
    arcpy.AddMessage("Joining outage points with service area")
    arcpy.SpatialJoin_analysis(serviceAreas,outages,serviceAreasJoin, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT")

    # print("Getting outages sorted by service area")
    # arcpy.AddMessage("Getting outages sorted by service area")
    # jCursor = sorted(arcpy.da.SearchCursor(serviceAreasJoin, ["ServArNu","Join_Count"]))
    # for jRow in jCursor:
    #     print("Service Area {}: {} outages".format(str(jRow[0]), str(jRow[1])))
    #     arcpy.AddMessage("Service Area {}: {} outages".format(str(jRow[0]), str(jRow[1])))
    # del jCursor

    # print("Getting outages sorted by total number of outages")
    arcpy.AddMessage("Getting outages sorted by total number of outages")
    jCursor = sorted(arcpy.da.SearchCursor(serviceAreasJoin, ["Join_Count", "ServArNu"]), reverse=True)
    for jRow in jCursor:
        # print("Service Area {}: {} outages".format(str(jRow[1]), str(jRow[0])))
        arcpy.AddMessage("Service Area {}: {} outages".format(str(jRow[1]), str(jRow[0])))
    del jCursor
    # print("Script complete")

except PhoneEmptyRows:
    # Message that the CSV file has not row values
    # print("Error: The {} file has no row values".format(xyFile))
    arcpy.AddError("Error: The {} file has no row values".format(xyFile))

except XyEmptyRows:
    # Message that the CSV file has not row values
    # print("Error: The {} file has no row values".format(pNumFile))
    arcpy.AddError("Error: The {} file has no row values".format(pNumFile))

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))

except Exception:
    e = sys.exc_info()[1]
    # print(e.args[0])
    arcpy.AddError(e.args[0])

# Add output to map
aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps("ScriptTool")[0]

m.addDataFromPath(outConvexHull)
m.addDataFromPath(outages)
densityLyr = arcpy.mp.LayerFile(r"C:\EsriTraining\PYTS\Data\OutageDensity.lyrx")
m.addLayer(densityLyr)
del aprx

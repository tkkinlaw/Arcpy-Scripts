import csv
import arcpy
import os
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = 103501

outage_csv = arcpy.GetParameterAsText(0)
parcels = arcpy.GetParameterAsText(1)
outage_area = arcpy.GetParameterAsText(2)
contact_fc = arcpy.GetParameterAsText(3)

outage_coords = []
csv_file = open(outage_csv)
csv_reader = csv.reader(csv_file)
next(csv_reader)
for row in csv_reader:
    outage_coords.append(row)

pnt_list = []
for coord in outage_coords:
    pnt = arcpy.Point(coord[0], coord[1])
    pnt_list.append(pnt)
pnt_ary = arcpy.Array(pnt_list)
outage_multipoint = arcpy.Multipoint(pnt_ary)

convex_hull = outage_multipoint.convexHull()
arcpy.CopyFeatures_management(convex_hull, outage_area)

path = os.path.normpath(contact_fc)
arcpy.CreateFeatureclass_management(os.path.split(contact_fc)[0], os.path.split(contact_fc)[1], "POINT")
arcpy.AddFields_management(contact_fc, [["Owner_Name", "TEXT"], ["Phone_Number", "TEXT"]])

with arcpy.da.SearchCursor(parcels, ["SHAPE@XY", "Owner_Name", "Phone_Number"]) as parcel_cursor:
    for parcel in parcel_cursor:
        pts = arcpy.Point((parcel[0])[0], (parcel[0])[1])
        parcel_geoms = arcpy.PointGeometry(pts)
        if parcel_geoms.within(convex_hull):
            cursor = arcpy.da.InsertCursor(contact_fc, 
                                           ["SHAPE@XY", "Owner_Name", "Phone_Number"])
            cursor.insertRow([((parcel[0])[0], (parcel[0])[1]), parcel[1], parcel[2]])
            del cursor
        else:
            continue

del parcel_cursor

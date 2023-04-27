import arcpy
import os

sourcePath = r"" #path to data location
csvFile = "ManholeCovers.csv"
csvPath = os.path.join(sourcePath, csvFile)
fc = os.path.join(sourcePath, "DemoData.gdb", "ManholeCovers_1")
print(csvPath)
print(fc)

# Here you will have to manually list the fields of interest. You could use Describe objects to extract them,
# which might be more appropriate depending on how many fields you are wanting to work with
targetFields = ["SHAPE@", "Asset_ID", "Status"]
sourceFields = []

# Just because we can, let's use a for loop and list function to create a list of the fields in the CSV file, excluding the OID field
flds = arcpy.ListFields("ManholeCovers.csv")
for fld in flds:
    if fld.name != "OID_":
        sourceFields.append(str(fld.name))
        print(fld.name)

csvCursor = arcpy.da.SearchCursor(csvPath, sourceFields)
fcCursor = arcpy.da.UpdateCursor(fc, targetFields)

# Count how many records are in the CSV file. This is how many updates will happen.
count = 0
for countRow in csvCursor:
    count += 1
print("There are " + str(count) + " edits to make") 

for uRow in fcCursor:
    uXY = uRow[0] #Feature class geometry object
    uAsset = uRow[1] #Feature class asset ID
    uStatus = uRow[2] #Feature class status, which needs updated
    for sRow in csvCursor:
        sX = sRow[0] #CSV file X coordinate
        sY = sRow[1] #CSV file Y coordinate
        sAsset = sRow[2] #CSV file asset ID
        sStatus = sRow[3] #CSV file status, which will be pushed to the matching feature
        if sAsset == uAsset:
            #Update the Geometry and Status fields
            uRow[0] = arcpy.Point(sX, sY)
            uRow[2] = sStatus
            fcCursor.updateRow(uRow)
            print("Asset number " + str(uAsset) + " has been updated")
        else:
            pass
    # That recent for loop reached the end of the cursor. Need to reset it for the next for loop iteration.
    csvCursor.reset()
print("The end")

del csvCursor
del fcCursor
print("All done")

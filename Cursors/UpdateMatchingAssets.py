import arcpy

arcpy.env.overwriteOutput = True

csvPath = r"C:\Users\tim10393\Desktop\CSVUpdateFC\Manhole_covers.csv"
fc = r"C:\Users\tim10393\OneDrive - Esri\DemoData\DemoData.gdb\ManholeCovers"

# Here you will have to manually list the fields of interest. You could use Describe objects to extract them,
# which might be more appropriate depending on how many fields you are wanting to work with
sourceFields = ["X", "Y", "Asset ID", "MHC Status"]
targetFields = ["SHAPE@", "Asset_ID", "Status"]

csvCursor = arcpy.da.SearchCursor(csvPath, sourceFields, where_clause = '"Asset ID" IS NOT NULL')
fcCursor = arcpy.da.UpdateCursor(fc, targetFields)

count = 0
for countRow in csvCursor:
    count += 1
del countRow
# Since we are using the same cursor later in the code, you need to reset the cursor back to the top
csvCursor.reset()

print("There are " + str(count) + " edits to make")
for uRow in fcCursor:
    uXY = uRow[0]
    uAsset = uRow[1]
    uStatus = uRow[2]
    for sRow in csvCursor:
        sX = sRow[0]
        sY = sRow[1]
        sAsset = sRow[2]
        sStatus = sRow[3]
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


# import site packages
import arcpy

# Set variables
fc = r"C:\EsriTraining\PYTS\Data\CountyData.gdb\ParcelPts"
# update value per square foot with update cursor
uFields = ['SquFoot', 'TaxValue', 'PriceSquFt']
with arcpy.da.UpdateCursor(fc, uFields) as uCursor:
    for row in uCursor:
        row[2] = row[1] / row[0]
        uCursor.updateRow(row)
# Search value per square foot for parcels to be reassessed
# Set variables for search cursor
sFields = ["Parcel_ID", "Owner_Name", "Phone_Number", "PriceSquFt"]
exp = '"PriceSquFt" <= 90'
# Populate the field names for the CSV file from the Search cursor
parcelList = ["Parcel_Id,Owner_Name,Phone_Number,PriceSquFt"]
with arcpy.da.SearchCursor(fc, sFields, exp) as sCursor:
    for row in sCursor:
        rowText = "{},{},{},{}".format(row[0], row[1], row[2], row[3])
        parcelList.append(rowText)
# Write messages to a CSV file
textBody = '\n'.join(parcelList)
csvFile = open(r"C:\EsriTraining\PYTS\AssessmentParcels.csv", "w")
csvFile.write(textBody)
csvFile.close()
print("Script Complete")

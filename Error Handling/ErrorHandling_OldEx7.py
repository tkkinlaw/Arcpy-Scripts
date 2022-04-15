# Create custom exception class
class EmptyRows(Exception):
    pass


# import modules
import arcpy
import csv
import sys

print("Modules imported.")
# variables
outageXY = r"C:\EsriTraining\PYTS\Data\OutageXY2.csv"
print("Variables are set.")
try:
    # Get count of rows in CSV
    csvCount = arcpy.GetCount_management(outageXY)
    if int(csvCount[0]) > 0:
        # Append coordinates from csv in a list and print the first row
        outageCoords = []
        csvFile = open(outageXY)
        csvReader = csv.reader(csvFile)
        next(csvReader)
        for row in csvReader:
            outageCoords.append(row)
        print(outageCoords[0])
    else:
        # Raise exception
        raise EmptyRows(csvCount)

except EmptyRows:
    # Message that the CSV file has not row values
    print("Error: The {} file has no row values".format(outageXY))

except arcpy.ExecuteError:
    print(arcpy.AddError(arcpy.GetMessages(2)))
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
print("Analysis complete.")
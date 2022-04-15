import arcpy

fc = r"C:\Demos\PYTS\SanDiego.gdb\GasStations"

with arcpy.da.SearchCursor(fc, "Shape@JSON") as sCursor:
    for row in sCursor:
        print(row[0])

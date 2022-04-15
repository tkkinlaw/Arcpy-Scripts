import arcpy
fc = r"C:\EsriTraining\PYTS\Demodata\SanDiego.gdb\GasStations"

flds = ["NAME", "ZIP_CODE","PUMPS"]

sqlExp = """PUMPS > 15"""

#where_clause=sqlExp,sql_clause=(None,"ORDER BY NAME"

with arcpy.da.SearchCursor(fc,flds,where_clause=sqlExp,sql_clause=(None,"ORDER BY NAME")) as src:
    for row in src:
        print("Name: {0}  Pumps: {2}  ZIP: {1}".format(row[0],row[1],row[2]))

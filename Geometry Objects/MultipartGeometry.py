import arcpy

fc = r"C:\Users\<replace>\DemoData\DemoData.gdb\WorldTerritories"
fields = ["NAME", "Shape@"]
whereClause = """NAME = 'United Kingdom'"""

src = arcpy.da.SearchCursor(fc, fields, where_clause = whereClause)
for row in src:
    print(row)

# The getPart method looks inside the polygon geometry object and grabs the first array of coordinates, being the
# geometry of one of the many territories of the United Kingdom
# By using this line of code outside the for loop, the row variable is set to the last iteration of the search cursor
# That is a good strategy for just testing code :)
arcpy.Polygon(row[1].getPart(0))


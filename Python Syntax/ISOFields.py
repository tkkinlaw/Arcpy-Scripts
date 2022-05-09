# Store the file path for the feature class
fc = r"C:\Users\tim10393\OneDrive - Esri\DemoData\DemoData.gdb\WorldTerritories"

# Generate a list of fields to use in the update cursor
flds = ["NAME", "SHAPE@", "ISOField"]

# Add a new field, which will later be populated with values
arcpy.management.AddField(in_table = fc, field_name = "ISOField", field_type = "TEXT")

# Sort through the feature class alphabetically according to the name of a country
cur = arcpy.da.UpdateCursor(fc, flds, sql_clause = (None, "ORDER BY NAME ASC"))

# We want to add three digits to the end of the territory name,
# starting with 001 -> 002 -> then 010 -> 011 -> then 201 -> 202,
# So, variable i will be our iterator. WIth each iteration of the for loop, it will increase by 1
i = 1
for row in cur:
    i += 1
    # Convert i to a string so that the leading zeros can be concatenated to it
    iso = str(i)
    if len(iso) == 1:
        iso = "00" + iso
    elif len(iso) == 2:
        iso = "0" + iso
    else:
        pass
    iso = str(row[0]) + iso
    # Update the row variable's ISOField value
    row[2] = iso
    print(row)
    # This method enforces the change, so it is reflected in the feature class
    cur.updateRow(row)
del cur
import arcpy
import os
arcpy.env.overwriteOutput = True

gdb = r"C:\Users\tim10393\Downloads\WorldTerritoriesSample.gdb"
fcName = "WorldTerritories"

fc = os.path.join(gdb, fcName)

#Data is from this site https://www.diva-gis.org/gdata and  the lines of code below, which, you can ignore:

arcpy.management.CreateFeatureclass(gdb, fcName, "POLYGON", r"C:\Users\tim10393\Downloads\WorldTerritoriesSample.gdb\AFG_adm1", "DISABLED", "DISABLED", 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision', '', 0, 0, 0, "World Territories")

arcpy.management.Append(r"C:\Users\tim10393\Downloads\WorldTerritoriesSample.gdb\AFG_adm1;C:\Users\tim10393\Downloads\WorldTerritoriesSample.gdb\ALA_adm1;C:\Users\tim10393\Downloads\WorldTerritoriesSample.gdb\ALB_adm1;C:\Users\tim10393\Downloads\WorldTerritoriesSample.gdb\MNG_adm1", r"C:\Users\tim10393\Downloads\WorldTerritoriesSample.gdb\WorldTerritories", "TEST", None, '', '')


# Add a new field to the feature class that will contain the desired result. Ex: MNG###
arcpy.management.AddField(in_table = fc, field_name = "ISOField", field_type = "TEXT")

#Create a list of the fields for the cursors
flds = ["NAME_0", "NAME_1", "SHAPE@", "ISOField", "ISO"]

# Create an empty list that you will add the unique values of the a field in a the feature class too
isoList = []

# Use the search cursor to access feature attributes.
with arcpy.da.SearchCursor(fc, flds) as src:
    for row in src:
        # Since we are interested in the unique vales of ISO values, check to see if the current iteration of the
        # search cursor is already in the list. If it is not in the list, then append it to the list
        if row[4] not in isoList:
            isoList.append(row[4])

print(isoList)

# The update cursor will calculate the new values and apply the edits
# We want to add three digits to the end of the ISO, with each territory having the same ISO code
# starting with 001 -> 002 -> then 010 -> 011 -> then 201 -> 202
# So, variable i will be our iterator. With each iteration of the for loop, it will increase by 1
cur = arcpy.da.UpdateCursor(fc, flds, sql_clause = (None, "ORDER BY NAME_0 ASC"))
i = 1
# Start by iterating over the list of ISO codes
for name in isoList:
    print("Processing " + name)
    # With the current ISO code from the list, iterate over the update cursor
    for row in cur:
        iso = str(i)
        # If the ISO field in the feature class matches the current ISO value from the list, then generate the code
        if row[4] == name:
            print(name)
            print(i)
            if len(iso) == 1:
                iso = "00" + iso
            elif len(iso) == 2:
                iso = "0" + iso
            else:
                pass
            # Genereate the ISO code and apply the changes
            isoName = str(row[4]) + iso
            row[3] = isoName
            cur.updateRow(row)
            print(row)
    # These two lines of code are outside the cursor's for loop sp that one all processing is done for a given
    # ISO from the list, increment the number by one for the next county/iteration of the parent for loop.
    i += 1
    # Since we have iterated over the update cursor (checking to see which rows match the country of interest),
    # we need to reset the cursor so that the next iteration of the parent for loop and use it from the beginning.
    cur.reset()


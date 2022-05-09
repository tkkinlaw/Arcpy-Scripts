import arcpy
demoGDB = r"C:\Demos\APEW\Demos.gdb"

arcpy.env.workspace = demoGDB
fcList = arcpy.ListFeatureClasses()
print(fcList)
print(len(fcList))

fcList2 = []
for fc in fcList:
    if "California" not in fc:
        fcList2.append(fc)
    else:
        print("Cali")

print(fcList2)
print(len(fcList2))


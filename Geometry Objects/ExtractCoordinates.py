fc = "ManHoleCovers"

geomList = ["x, y"]
for row in arcpy.da.SearchCursor(fc, ["SHAPE@XY"]):
    x, y = row[0]
    coords = "{}, {}".format(x, y)
    geomList.append(coords)

textBody = '\n'.join(geomList)
csvFile = open(r"C:\Demos\PYTS\Manhole_covers{}.csv".format(fc), "w")
csvFile.write(textBody)
csvFile.close()

import datetime
import arcpy

arcpy.env.overwriteOutput = True

now = datetime.datetime.now()

year = now.strftime("%Y")
print("year:", year)

month = now.strftime("%m")
print("month:", month)

day = now.strftime("%d")
print("day:", day)

todayDate = year + "_" + month + "_" + day
print(todayDate)

fc = r"C:\Demos\PYTS\SanDiego.gdb\GasStations"
name = "NewGasStations_"
outPath = name + todayDate
print(outPath)
arcpy.conversion.FeatureClassToFeatureClass(in_features = fc,
                                            out_path = r"C:\Demos\PYTS\SanDiego.gdb",
                                            out_name = outPath)
# coding: utf-8
# Import site package
import arcpy

print("arcpy site package imported")
arcpy.env.overwriteOutput = True
# Set variables
output = r"C:\EsriTraining\PYTS\Default.gdb\AffectedAreaAppCurrent"
area = r"C:\EsriTraining\PYTS\Default.gdb\AffectedArea"
distance = "0.5 Miles"
shpInput = r"C:\EsriTraining\PYTS\Data\AffectedAreaApp.shp"
print("Variables set")
# Add shapefile to geodatabase
#arcpy.management.CopyFeatures("AffectedAreaApp", output)
arcpy.management.CopyFeatures(shpInput, output)
print("Shapefile imported into geodatabase")
# Create buffer from points
arcpy.analysis.Buffer(output, area, distance, "FULL", "ROUND", "ALL", None, "PLANAR")
print("Buffer created \nScript complete")

# coding: utf-8
#import site package
import arcpy

print("arcpy site package imported")
arcpy.env.overwriteOutput = True
#Set variables
output = r"C:\EsriTraining\PYTS\Default.gdb\AffectedAreaAppCurrent"
rasterName = r"C:\EsriTraining\PYTS\Default.gdb\KernelDensityOutage"
shpInput=r"C:\EsriTraining\PYTS\Data\AffectedAreaApp.shp"
print("Variables set")
#Add shapefile to geodatabase
#arcpy.management.CopyFeatures('AffectedAreaApp', output)
arcpy.management.CopyFeatures(shpInput,output)
print("Shapefile imported into geodatabase")
#Calculate kernel density from points
outKD = arcpy.sa.KernelDensity(output, 'NONE')
outKD.save(rasterName)
print("Kernel density calculated \nScript complete")

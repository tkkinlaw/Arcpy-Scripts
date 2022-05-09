import arcpy
import os

workspace = r"C:\Users\tim10393\OneDrive - Esri\DemoData\Imagery Data\NAIP\Texas\2020"
rasters = []

walk = arcpy.da.Walk(workspace, datatype="RasterDataset")

for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        rasters.append(os.path.join(dirpath, filename))
print(rasters)
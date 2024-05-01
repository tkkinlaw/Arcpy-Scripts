'''
We want to create a mosaic dataset, add rasters to it.
All rasters are in the same root folder,
but each in their own sub-folder.
Then, calculate footprints for the mosaic dataset

Plan the code. What tools are needed, and in what order.
What arcpy functions might we need?
If you know the syntax - great! Otherwise, just do the "plan code" and "explore syntax" steps of the python script creation workflow.
'''
#Import packages
import arcpy

#Set environment
rootFolder = r"C:\Users\tim10393\OneDrive - Esri\DemoData\Imagery Data\NAIP\Texas\2020"
arcpy.env.workspace = rootFolder

#List Rasters
rasterList = []
foldersWRasters = []
listFolders = arcpy.ListFiles()
for folder in listFolders:
    desc = arcpy.Describe(folder)
    
    if desc.extension == 'ZIP':
        pass
    else:
        fullFolderPath = f"{rootFolder}\{folder}"
        foldersWRasters.append(fullFolderPath)

for folder in foldersWRasters:
    arcpy.env.workspace = folder
    listRasters = arcpy.ListRasters()
    for raster in listRasters:
        fullFolderPath = f"{folder}\{raster}"
        rasterList.append(fullFolderPath)
print(len(rasterList))

# Create geodatabase
gdbLoc = r"C:\Users\tim10393\OneDrive - Esri\DemoData\Imagery Data\NAIP\Texas"
gdbName = "NAIP_TX_2020"
gdbPath = f"{gdbLoc}\{gdbName}.gdb"
print(gdbPath)
if arcpy.Exists(gdbPath):
    pass
else:
    arcpy.management.CreateFileGDB(out_folder_path=gdbLoc, out_name=gdbName)

#Create Mosaic
mdName = "Yeehaw"
md = f"{gdbPath}\{mdName}"
print(md)
sp = arcpy.SpatialReference(26914)
if arcpy.Exists(md):
    pass
else:
    arcpy.management.CreateMosaicDataset(in_workspace=gdbPath, in_mosaicdataset_name=mdName, coordinate_system=sp)
    print(f"{mdName} Mosaic dataset created")

#Add rasters to mosaic
arcpy.management.AddRastersToMosaicDataset(
    in_mosaic_dataset=md,
    raster_type="Raster Dataset",
    input_path=rasterList)
print("Rasters added")
#calculate footprints
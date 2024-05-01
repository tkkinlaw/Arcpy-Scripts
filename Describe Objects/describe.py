import arcpy

fc = r"C:\Demo\PYTS\SanDiego.gdb\MajorAttractions"

desc = arcpy.Describe(fc)

print(desc)

print(desc.shapeType)

if desc.shapeType == "Point" and desc.datasetType == "FeatureClass":
	arcpy.CreateFeatureclass_management(out_path=desc.path,
                                   out_name="DownTown{}".format(desc.name), geometry_type="POLYGON", template=fc,
                                    spatial_reference=desc.spatialReference)

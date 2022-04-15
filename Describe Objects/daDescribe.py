import arcpy

fc = r"C:\Demos\PYTS\SanDiego.gdb\MajorAttractions"

daDesc = arcpy.da.Describe(fc)

print(daDesc)

print(daDesc['shapeType'])

if 'Point' in daDesc.values() and 'FeatureClass' in daDesc.values():
    print(daDesc['path'])
    arcpy.CreateFeatureclass_management(out_path=daDesc['path'],
                                        out_name="DownTown{}".format(daDesc['name']),
                                        geometry_type="POLYGON", template=fc,
                                        spatial_reference=daDesc['spatialReference']) 



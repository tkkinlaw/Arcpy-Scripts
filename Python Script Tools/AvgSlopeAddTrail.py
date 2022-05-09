import arcpy
import os

arcpy.env.overwriteOutput = True

inGPX = arcpy.GetParameterAsText(0)
targetFC = arcpy.GetParameterAsText(1)
elevation = arcpy.GetParameterAsText(2)
outLayer = arcpy.GetParameterAsText(3)
tempFC = r"in_memory/GPXToFeatures"
prjFC = os.path.join(arcpy.env.scratchGDB, "tempPrjFeature")

#Convert the GPX file to a temporary feature class
arcpy.conversion.GPXtoFeatures(inGPX, tempFC, "TRACKS_AS_LINES")
print("Converting GPX to Features")

#Project the GPX features in to the proper CRS
desc = arcpy.Describe(targetFC)
arcpy.management.Project(tempFC, prjFC, desc.spatialReference)
print("Projecting the feature to: ", desc.spatialReference.name)

#Update the Length field for the temporary feature. The target feature class has this attribute.

arcpy.management.AddField(prjFC, "Length_Mi", "DOUBLE", None, None, None, "Length", "NULLABLE", "NON_REQUIRED", '')
print("Field added")
arcpy.management.CalculateGeometryAttributes(prjFC, "Length_Mi LENGTH_3D", "MILES_US", '', desc.spatialReference)
print("3D length calculated")

#Update Feature Z geometry from more accurate source
arcpy.ddd.UpdateFeatureZ(prjFC, elevation, "BILINEAR", None)
print("Updating the feature's z value")

#Add the average slope of the feature
arcpy.ddd.AddSurfaceInformation(prjFC, elevation, "AVG_SLOPE", "BILINEAR", None, 1, 0, '')
print("Calculating the average slope of the feature")

#Update the value from the GPX file to match the name of the downloaded file.
updateCur = arcpy.da.UpdateCursor(prjFC, "Name")
nameGPX = os.path.basename(inGPX)
nameNoExt = nameGPX.replace(".gpx","")
for row in updateCur:
    row[0] = nameNoExt
    updateCur.updateRow(row)
del updateCur

#Append the new trail to the existing trails feature class
arcpy.management.Append(prjFC, targetFC, schema_type = "NO_TEST")
print("Appending the new trail to the existing feature class")

#Delete the scratch GDB
arcpy.Delete_management(tempFC)
print("Deleting intermediate data")

#Since there is no new Feature class persisted, a layer needs created so it can be added to the map automatically
arcpy.MakeFeatureLayer_management(targetFC, outLayer)
print("All done")


# We have a geodatabase of two feature classes
# We want to create a feature data set, add these two feature classes to it, and create a topology using those two FCs.
# We want to add a topology rule that checks for where polygons (City boundaries) are not inside another polygon (State)
# We then want to validate the topology
# Then we will export the features violating the topology rule
# Then transfer the attributes of the City violating the rule to the exported results, since they got dropped.
### Next steps
# Then, add another feature class to the topology. Bring another FC into the topology
# OR/AND apply the topology to the new FC.
import arcpy
import os
import datetime
arcpy.env.overwriteOutput = True

basePath = r"C:\Users\student\Desktop\PYTS" # This is the common directory all data lives for this script

ncGDBName = "NorthCarolina.gdb" # Geodatabase containing the data to start with.
ncGDB = os.path.join(basePath, ncGDBName) # This is the full filepath to the source geodatabase

fdName = 'NCCities' # Name of the feature dataset to be created
topologyName = 'NCCitiesToState' # Name of the topology dataset to be created

cities = 'NCDOT_City_Boundaries_FD' # Name of a feature class from feature dataset to participate in the topology
state = 'NC_SPCS_FD' # Name of a feature class from feature dataset to participate in the topology

errorGDBName = "TopologyErrors" # This is the name of the geodatabase storing topology errors
errorGDB = os.path.join(basePath, errorGDBName+".gdb") # This is the full file path to the geodatabase storing topology errors

timeStamp = datetime.datetime.now().strftime("%d%b%Y_%H_%M_%S")
topoErrorsFcName = cities+state+"_errors_"+timeStamp # This is the name of the exported topology errors
outputSJ = os.path.join(errorGDB, topoErrorsFcName+"_Attributes") # The final result is from a spatial join. We want this in the errorGDBName geodatabase
print("Variables set")

# Describe a feature class so we can extract the desired spatial reference
arcpy.env.workspace = ncGDB
fcList = arcpy.ListFeatureClasses()
print(fcList[0])
desc = arcpy.Describe(fcList[0])
print(f"Using this spatial reference {desc.spatialReference.name}")
sp = desc.spatialReference
# Create a feature dataset
arcpy.management.CreateFeatureDataset(out_dataset_path=ncGDB,out_name=fdName,spatial_reference=sp)
print(f"Feature dataset created in {ncGDB}")

# Add feature classes to the feature dataset
for fc in fcList:
    copiedFeat = os.path.join(ncGDB, fdName, fc + "_FD")
    print(f"Output is: {copiedFeat}")
    arcpy.conversion.ExportFeatures(in_features=fc, out_features=copiedFeat)

# Create topology in the feature dataset
arcpy.management.CreateTopology(in_dataset=fdName, out_name=topologyName)
print("Topology created")

# Add feature classes to a topology
arcpy.env.workspace = os.path.join(ncGDB,fdName)
print(arcpy.env.workspace)
fcInFDList = arcpy.ListFeatureClasses()
print(fcInFDList)
for fcFromFD in fcInFDList:
    print(fcFromFD)
    arcpy.management.AddFeatureClassToTopology(in_topology=topologyName, in_featureclass=fcFromFD, xy_rank=1, z_rank=1)
    print("Feature class added to topology")

# Now that we have FCs in a topology, let's add a rule to the topology
arcpy.management.AddRuleToTopology(in_topology=topologyName,
                                   rule_type="Must Be Covered By Feature Class Of (Area-Area)",
                                   in_featureclass=cities,
                                   in_featureclass2=state)
print("Topology rule added")

# Validate topology
r = arcpy.management.ValidateTopology(in_topology=topologyName)
print("Topology validated")

# Now, let's print the NC Cities that are violating our topology rule.
# We need to use the Export Topology Errors geoprocessing tool to do this.
# We need to make sure we have a geodatabase created to store the output
if arcpy.Exists(errorGDB):
    print(f"There is already a geodatabase at {errorGDB}. Exporting errors")
else:
    arcpy.management.CreateFileGDB(basePath, errorGDBName)
    print(f"{errorGDBName} created. Exporting errors")

arcpy.management.ExportTopologyErrors(in_topology=topologyName, out_path=errorGDB, out_basename=topoErrorsFcName)
print(f"{topoErrorsFcName} created. You can now see the topology errors at: {errorGDB}")

# Exporting topology errors does not export attribute data. Let's use spatial join to transfer the attribute data based
# on the spatial relationship of the original data (containing the attribute data) and the output errors feature class
print("Adding original attribute data to output error feature class")

arcpy.analysis.SpatialJoin(target_features=cities,
                           join_features=state,
                           out_feature_class=outputSJ,
                           match_option="WITHIN")
print("All done")
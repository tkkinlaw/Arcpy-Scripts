# We have a geodatabase of two feature classes
# We want to create a feature data set and a topology for those two FCs.
# We then want to validate the topology
# Then, add another feature class to the topology. Bring another FC into the topology
# OR/AND apply the topology to the new FC.
import arcpy, os
arcpy.env.overwriteOutput = True
ncGDB = r"C:\Users\student\Desktop\PYTS\NorthCarolina.gdb"
fdName = 'NCCities'
topologyName = 'NCCitiesToState'
cities = 'NCDOT_City_Boundaries_FD'
state = 'NC_SPCS_FD'
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
arcpy.management.ValidateTopology(in_topology=topologyName)
print("Topology validated")
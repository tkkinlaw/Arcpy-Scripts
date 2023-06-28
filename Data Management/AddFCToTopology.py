import arcpy
import os

#topo = r"C:\Users\student\Desktop\PYTS\NorthCarolina.gdb\NCCities\NCCitiesToState"
#fcToCheck = r"C:\Users\student\Desktop\PYTS\NorthCarolina.gdb\NCCities\NC_Census_Tracts_FD"
#state = r"C:\Users\student\Desktop\PYTS\NorthCarolina.gdb\NCCities\NC_SPCS_FD"

topo = arcpy.GetParameterAsText(0)
fcToCheck = arcpy.GetParameterAsText(1) # This feature class should NOT live in the feature dataset
state = arcpy.GetParameterAsText(2)
outPath = arcpy.GetParameterAsText(3) # Output location for topology errors
outName = arcpy.GetParameterAsText(4) # Output name for topology errors
overwrite = arcpy.GetParameter(5)

descFc = arcpy.Describe(fcToCheck)

descTopo = arcpy.Describe(topo)
arcpy.AddMessage(f"These are the feature classes participating in the topology: {descTopo.featureClassNames}")

# Check to see if the input feature class (in the FD) is in the topology
fcTopoNum = len(descTopo.featureClassNames)

# Check to see if the input feature class is in the feature datset or not. 
# To do this, we will grab the catalog path for the feature dataset. If the number of backslashes in the 
# filepath is 2, then it is in a feature dataset. Otherwise, it is not.
backSlashNum = descFc.catalogPath.split('.gdb')[1].count("\\")
fdPath = 
if backSlashNum == 2:
    newFC = os.path.join(descTopo.path, fcToCheck + "_FD")
    arcpy.management.ExportFeatures(fcToCheck, newFC)
    fcToCheck = newFC # DOUBLE CHECK THIS

# Check to see if the input feature class is in the topology. If it is, and the user allowed the tool to overwrite,
# then remove this feature class from the topology, then proceed with the script.
if descFc.name in descTopo.featureClassNames and overwrite:
    arcpy.AddMessage(f"Removing {fcToCheck} from the topology")
    arcpy.management.RemoveFeatureClassFromTopology(in_topology=topo,in_featureclass=fcToCheck)
if fcTopoNum == 0:
    arcpy.AddMessage("There are no feature classes participating in this topology.")
elif fcTopoNum == 1:
    arcpy.AddMessage("There is only one feature class in this topology.")
elif fcTopoNum > 1:
    arcpy.AddMessage(f"There are {fcTopoNum} feature classes participating in the topology.")
    if descFc.name not in descTopo.featureClassNames:
        arcpy.AddMessage(f"Adding {descFc.name} to the topology")
        # Add the feature class to the topology
        arcpy.management.AddFeatureClassToTopology(in_topology=topo, in_featureclass=fcToCheck, xy_rank=1, z_rank=1)
        # Add a rule to the newly added feature class
        arcpy.management.AddRuleToTopology(in_topology=topo,rule_type="Must Be Covered By Feature Class Of (Area-Area)",in_featureclass=fcToCheck,in_featureclass2=state)
    else:
        arcpy.AddMessage(f"{descFc.name} is already participating in the topology")
# Validate topology
arcpy.management.ValidateTopology(in_topology=topo)
arcpy.AddMessage("Topology validated")
arcpy.management.ExportTopologyErrors(in_topology=topo, out_path=outPath, out_basename=outName)
arcpy.AddMessage("Topology errors exported")
import arcpy
import os
from datetime import datetime

topo = r"C:\Demos\PYTS\NorthCarolina.gdb\NCCities\NCCitiesToState"
fcToCheck = r"C:\Demos\PYTS\NorthCarolina.gdb\NC_Census_Tracts"
state = r"C:\Demos\PYTS\NorthCarolina.gdb\NCCities\NC_SPCS_FD"
outPath = r"C:\Demos\PYTS\TopologyErrors.gdb"
outName = "Test"
overwrite = True

#To turn this into a Python script tool, comment out the lines of code above and use the ones below.
#topo = arcpy.GetParameterAsText(0)
#fcToCheck = arcpy.GetParameterAsText(1) # This feature class should NOT live in the feature dataset
#state = arcpy.GetParameterAsText(2)
#outPath = arcpy.GetParameterAsText(3) # Output location for topology errors
#outName = arcpy.GetParameterAsText(4) # Output name for topology errors
#overwrite = arcpy.GetParameter(5)

descFc = arcpy.Describe(fcToCheck)
descTopo = arcpy.Describe(topo)
arcpy.AddMessage(f"These are the feature classes participating in the topology: {descTopo.featureClassNames}")


# This creates a unique name for the input feature class in the feature dataset. It adds the timestamp.
outFCFDName = os.path.join(descTopo.path, descFc.name+datetime.now().strftime('%d%b%Y_%H_%M_%S'))
arcpy.conversion.ExportFeatures(fcToCheck, outFCFDName)
fcToCheck = outFCFDName

fcTopoNum = len(descTopo.featureClassNames)

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

arcpy.AddMessage("Validating topology")
arcpy.management.ValidateTopology(in_topology=topo)

if arcpy.Exists(outPath):
    pass
else:
    arcpy.management.CreateFileGDB(outPath)

arcpy.AddMessage(f"Exporting topology errors to {outPath}")
arcpy.management.ExportTopologyErrors(in_topology=topo, out_path=outPath, out_basename=outName)


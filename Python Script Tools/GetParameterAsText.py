import arcpy

arcpy.env.overwriteOutput = True

input = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

arcpy.analysis.Buffer(input, output, "50 feet")

desc = arcpy.Describe(input)

arcpy.AddMessage("Congrats! You just made a 50 foot buffer for this dataset: " + desc.name)

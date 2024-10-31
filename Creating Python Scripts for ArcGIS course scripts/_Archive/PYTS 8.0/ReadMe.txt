Remember, the arcpy.GetParameter and arcpy.GetParameterAsText functions determine what Python object is sent to your Python Script. The end-user interacts with your python script via the Python Script Tool interface in the Geoprocessing pane. In the parameter tab of the Python Script tool properties, you can help the end-user supply the input parmaters by specifying the data type required for each parameter. 

Examples:
- You keep this default data type for a parameter. This is a string.
	- This means the user needs to type in a string (ex. a file path)
	- If your python script uses arcpy.GetParameter(), the variable holding the input parameter will be a string.
	- If your python script uses arcpy.GetParameterAsText(), the variable holding the input parameter will be a string.
- You change the data type to FeatureClass. This enables to end-user to click a folder in the geoprocessing pane and select a feature class (famliar and what we see in most out-of-the-box geoprocessing tools):
	- If your python script uses arcpy.GetParameter(), the variable holding the input parameter will be a type of python object arcpy determines.
	- If your python script uses arcpy.GetParameterAsText(), the variable holding the input parameter will be a string.
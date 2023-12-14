import arcpy
import sys

arcpy.env.workspace = r"C:\EsriTraining\PYTS\Data\CountyData.gdb"
try:
    # Execute the Buffer tool
    arcpy.Buffer_analysis("ParcelPts", "ParcelPtsBuffer") #this buffer tool is missing the distance/field parameter, causing the script to return an error
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])

    # If using this code within a script tool, AddError can be used to return messages
    #   back to a script tool. If not, AddError will have no effect.
    #arcpy.AddError(e.args[0])
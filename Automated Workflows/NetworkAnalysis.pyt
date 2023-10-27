# -*- coding: utf-8 -*-
import arcpy
from pprint import pprint
import os

class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Network Analysis"
        self.alias = "NetworkAnalysis"

        # List of tool classes associated with this toolbox
        self.tools = [FastestRoute]


class FastestRoute:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Fastest Route"
        self.description = "This tool generates the fastest route between two points."

    def getParameterInfo(self):
        """Define the tool parameters."""
        inputCoord = arcpy.Parameter(
        displayName="Starting Location",
        name="Starting_Location",
        datatype="GPFeatureRecordSetLayer",
        parameterType="Required",
        direction="Input")

        outRoute = arcpy.Parameter(
        displayName="Output Route Name",
        name="Output_Route_Name",
        datatype="GPNALayer",
        parameterType="Required",
        direction="Output")

        params = [inputCoord,outRoute]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Declare variables
        naxName = str(parameters[1].value)
        arcpy.AddMessage(naxName)
        inputCoords = []
        sCur = arcpy.da.SearchCursor(parameters[0].value, "Shape@XY")
        for row in sCur:
            arcpy.AddMessage(row[0])
            inputCoords.append(row[0])
        del sCur
        arcpy.AddMessage(parameters[0].value)
        gdb = r"C:\Users\tim10393\Documents\ArcGIS\Projects\NetworkAnalysis\Default.gdb"
        inBarFcName = "Barriers"
        inStopFcName = "StopsFc" 
        inStopFc = os.path.join(gdb, inStopFcName)

        arcpy.env.workspace = gdb
        arcpy.env.overwriteOutput = True
        arcpy.env.addOutputsToMap = True

        #Create a table
        arcpy.management.CreateFeatureclass(out_path=gdb, out_name=inStopFcName, geometry_type="Point", spatial_reference=4326)

        # Provide input stop data for the insert cursor
        cur = arcpy.da.InsertCursor(inStopFcName, ["Shape@"])
        for coord in inputCoords:
            pnt = arcpy.Point(coord[0],coord[1])
            pntGeom = arcpy.PointGeometry(pnt)
            cur.insertRow([pntGeom])
        del cur

        #Create the analysis layer
        naxLyr = arcpy.na.MakeRouteAnalysisLayer(
            network_data_source="https://www.arcgis.com/",
            layer_name=naxName)
        print("Network analysis layer created")

        # Add the stop locations
        arcpy.na.AddLocations(
            in_network_analysis_layer=naxLyr,
            sub_layer="Stops",
            in_table=inStopFc)
        print("Input locations added")

        # Add the barriers
        arcpy.na.AddLocations(
            in_network_analysis_layer=naxLyr,
            sub_layer="Polygon Barriers",
            in_table=inBarFcName)
        print("Barriers added")

        # Solve the problem
        arcpy.na.Solve(
            in_network_analysis_layer=naxLyr)
        print("Problem solved")

        arcpy.management.Delete(inStopFc)

        arcpy.AddMessage(arcpy.da.Describe(naxLyr[0]))
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

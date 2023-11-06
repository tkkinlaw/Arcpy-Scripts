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
        datatype="GPString",
        parameterType="Required",
        direction="Output")

        outFC = arcpy.Parameter(
        displayName="Output Route",
        name="Output_Route",
        datatype="DEFeatureClass",
        parameterType="Required",
        direction="Output")
        
        params = [inputCoord,outRoute,outFC]
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

        arcpy.AddMessage(arcpy.env.scratchGDB)
        
        gdb = arcpy.env.scratchGDB
        inBarFcName = "Barriers"
        inStopFcName = "StopsFc" 
        inStopFc = os.path.join(gdb, inStopFcName)

        arcpy.env.workspace = gdb
        arcpy.env.overwriteOutput = True

        #Create a table
        arcpy.management.CreateFeatureclass(out_path=gdb, out_name=inStopFcName, geometry_type="Point", spatial_reference=3857)

        # Provide input stop data for the insert cursor
        cur = arcpy.da.InsertCursor(inStopFcName, ["Shape@"])
        for coord in inputCoords:
            pnt = arcpy.Point(coord[0],coord[1])
            pntGeom = arcpy.PointGeometry(pnt)
            cur.insertRow([pntGeom])
        del cur

        # Try signing in with Python 
        arcpy.SignInToPortal("Your Portal","Your Username","Your Password")

        #Create the analysis layer
        naxLyr = arcpy.na.MakeRouteAnalysisLayer(
            network_data_source="https://adsrv2019.ad.local/portal/",
            layer_name=naxName)
        print("Network analysis layer created")
        naxLyr.getOutput(0)

        # Add the stop locations
        arcpy.na.AddLocations(
            in_network_analysis_layer=naxLyr,
            sub_layer="Stops",
            in_table=inStopFc)
        print("Input locations added")

        # Solve the problem
        arcpy.na.Solve(
            in_network_analysis_layer=naxLyr)
        print("Problem solved")

        d = arcpy.da.Describe(naxLyr.getOutput(0))
        for dictionary in d['children']:
            if "Route" in dictionary['name']:
                routeFC_FD = dictionary['catalogPath']
                print(routeFC_FD)

        arcpy.management.CopyFeatures(routeFC_FD, parameters[2].value)
        arcpy.AddMessage("Output created")
        delFD = os.path.split(d['children'][0]['catalogPath'])[0]
        arcpy.management.Delete([delFD,inStopFc])
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

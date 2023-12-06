# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "First python toolbox label"
        self.alias = "First python toolbox description"

        # List of tool classes associated with this toolbox
        self.tools = [BufferPYT]


class BufferPYT(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "This is the first python toolbox label"
        self.description = "This is the first python toolbox description"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramInFeatures = arcpy.Parameter(
        displayName="Features to buffer",
        name="Feature_To_Buffer",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Input")

        paramOutBuffer = arcpy.Parameter(
        displayName="Output buffer",
        name="Output_Buffer",
        datatype="DEFeatureClass",
        parameterType="Required",
        direction="Output")

        paramDate = arcpy.Parameter(
        displayName="Date",
        name="Date",
        datatype="GPDate",
        parameterType="Required",
        direction="Input")

        params = [paramInFeatures,paramOutBuffer,paramDate]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Perform the analysis
        arcpy.analysis.Buffer(parameters[0].value, parameters[1].valueAsText+parameters[2].value.strftime("%Y%m%d"), "1 Mile")
        arcpy.AddMessage("Buffer analysis is complete!")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

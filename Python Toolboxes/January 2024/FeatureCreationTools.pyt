# -*- coding: utf-8 -*-

import arcpy
import csv
import arcgis
from arcgis.gis import GIS

class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Demo python toolbox"
        self.alias = "Demo python toolbox".replace(" ", "")

        # List of tool classes associated with this toolbox
        self.tools = [Tool,Testing]


class Tool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create features from Table"
        self.description = "This inserts values into a feature layer. Works with portal."

    def getParameterInfo(self):
        """Define the tool parameters."""

        direction = 'Input'
        paramType = "Required"

        targetFeatureLayer = arcpy.Parameter(name = "Target_Feature_Layer",
                                             displayName = "Target_Feature_Layer".replace("_"," "),
                                             direction=direction,
                                             datatype="GPFeatureLayer",
                                             parameterType=paramType) 
        csvFile = arcpy.Parameter(name = "Input_Table",
                                  displayName = "Input Table",
                                  direction=direction,
                                  datatype="DETable",
                                  parameterType=paramType) 
        csvSP = arcpy.Parameter(name = "Input_Coordinate_Spatial_Reference",
                                displayName="Input_Coordinate_Spatial_Reference".replace("_"," "),
                                direction=direction,
                                datatype="GPSpatialReference",
                                parameterType=paramType) 
        csvXField = arcpy.Parameter(name = "X Field",
                                    displayName="X_Field",
                                    direction=direction,
                                    datatype="Field",
                                    parameterType=paramType) 
        csvYField = arcpy.Parameter(name = "Y Field",
                                    displayName="Y_Field",
                                    direction=direction,
                                    datatype="Field",
                                    parameterType=paramType)  
        
        # Set up parameter Dependencies
        csvXField.parameterDependencies = [csvFile.name]
        csvYField.parameterDependencies = [csvFile.name]
 
        params = [targetFeatureLayer,csvFile,csvSP,csvXField,csvYField]
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

        targetFeatureLayer = parameters[0].valueAsText
        csvFile = parameters[1].valueAsText
        csvSP = parameters[2].value
        csvXField = parameters[3].valueAsText
        csvYField = parameters[4].valueAsText

        gis = GIS("Pro")
        print("Signed in!")

        arcpy.env.overwriteOutput=True
        crimeLyr = arcpy.management.MakeFeatureLayer(
            in_features=targetFeatureLayer,
            out_layer="CrimePoints",
            where_clause="",
            workspace=None,
            field_info="OBJECTID OBJECTID VISIBLE NONE;IncidentName IncidentName VISIBLE NONE;Time_stamp Time_stamp VISIBLE NONE;Shape Shape VISIBLE NONE"
        )

        fieldNames = ['IncidentName','Time_stamp',"Shape@XY"]
        iCur = arcpy.da.InsertCursor(crimeLyr[0],fieldNames)

        file = open(csvFile)
        csvData = csv.reader(file)
        next(csvData)

        targetSP = arcpy.da.Describe(crimeLyr[0])['spatialReference']
        arcpy.AddMessage(targetSP.name)

        for row in csvData:
            print(row)
            pnt = arcpy.Point(row[2],row[3])
            pntGeom = arcpy.PointGeometry(pnt, spatial_reference=csvSP)
            pntGeom = pntGeom.projectAs(targetSP)
            iName = None
            timeStamp = row[1]
            iRow = [iName, timeStamp, (pntGeom.centroid.X, pntGeom.centroid.Y)]
            iCur.insertRow(iRow)
        del iCur, csvData





        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return


class Testing:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create features from Table2"
        self.description = "This inserts values into a feature layer. Works with portal."

    def getParameterInfo(self):
        """Define the tool parameters."""

        direction = 'Input'
        paramType = "Required"

        targetFeatureLayer = arcpy.Parameter(name = "Target_Feature_Layer",
                                             displayName = "Target_Feature_Layer".replace("_"," "),
                                             direction=direction,
                                             datatype="GPFeatureLayer",
                                             parameterType=paramType) 
        csvFile = arcpy.Parameter(name = "Input_Table",
                                  displayName = "Input Table",
                                  direction=direction,
                                  datatype="DETable",
                                  parameterType=paramType) 
        csvSP = arcpy.Parameter(name = "Input_Coordinate_Spatial_Reference",
                                displayName="Input_Coordinate_Spatial_Reference".replace("_"," "),
                                direction=direction,
                                datatype="GPSpatialReference",
                                parameterType=paramType) 
        csvXField = arcpy.Parameter(name = "X Field",
                                    displayName="X_Field",
                                    direction=direction,
                                    datatype="Field",
                                    parameterType=paramType) 
        csvYField = arcpy.Parameter(name = "Y Field",
                                    displayName="Y_Field",
                                    direction=direction,
                                    datatype="Field",
                                    parameterType=paramType) 

        fieldMatching = arcpy.Parameter(name = "Fields to match",
                                        displayName="Fields_to_match",
                                        direction=direction,
                                        datatype="GPValueTable",
                                        parameterType=paramType) 
        
        fieldMatching.parameterDependencies = [targetFeatureLayer.name, csvFile.name]
        fieldMatching.columns = [['Field', 'Input Field'], ['Field', 'Target Field']]
        fieldMatching.filters[0].type = 'ValueList'
        fieldMatching.filters[1].type = 'ValueList'
        #fieldMatching.values = [['NAME', 'SUM']]
        #fieldMatching.filters[1].list = ['SUM', 'MIN', 'MAX', 'STDEV', 'MEAN']

        # Set up parameter Dependencies
        #csvXField.parameterDependencies = [csvFile.name]
        #csvYField.parameterDependencies = [csvFile.name]
 
        params = [targetFeatureLayer,csvFile,csvSP,csvXField,csvYField,fieldMatching]
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

        targetFeatureLayer = parameters[0].valueAsText
        csvFile = parameters[1].valueAsText
        csvSP = parameters[2].value
        csvXField = parameters[3].valueAsText
        csvYField = parameters[4].valueAsText
        fieldMatching = parameters[5].value

        gis = GIS("Pro")
        print("Signed in!")

        arcpy.env.overwriteOutput=True
        crimeLyr = arcpy.management.MakeFeatureLayer(
            in_features=targetFeatureLayer,
            out_layer="CrimePoints",
            where_clause="",
            workspace=None,
            field_info="OBJECTID OBJECTID VISIBLE NONE;IncidentName IncidentName VISIBLE NONE;Time_stamp Time_stamp VISIBLE NONE;Shape Shape VISIBLE NONE"
        )

        fieldNames = ['IncidentName','Time_stamp',"Shape@XY"]
        iCur = arcpy.da.InsertCursor(crimeLyr[0],fieldNames)

        file = open(csvFile)
        csvData = csv.reader(file)
        next(csvData)

        targetSP = arcpy.da.Describe(crimeLyr[0])['spatialReference']
        arcpy.AddMessage(targetSP.name)

        for row in csvData:
            print(row)
            pnt = arcpy.Point(row[2],row[3])
            pntGeom = arcpy.PointGeometry(pnt, spatial_reference=csvSP)
            pntGeom = pntGeom.projectAs(targetSP)
            iName = None
            timeStamp = row[1]
            iRow = [iName, timeStamp, (pntGeom.centroid.X, pntGeom.centroid.Y)]
            iCur.insertRow(iRow)
        del iCur, csvData





        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

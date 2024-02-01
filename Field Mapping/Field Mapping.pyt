# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Field Mapping tool"
        self.alias = "FieldMappingTool"

        # List of tool classes associated with this toolbox
        self.tools = [UpdateFromMatchingFields]

class UpdateFromMatchingFields:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Update FC with Table"
        self.description = "This Python Toolbox uses the ValueTable data type to enable the end user to map together source and target fields to update a feature class from a table."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        inputDirection = "Input"
        reqParamType = "Required"

        targetFCParam = arcpy.Parameter(
            name="Target_Feature_Class",
            displayName="Target Feature Class",
            direction=inputDirection,
            datatype="GPFeatureLayer",
            parameterType=reqParamType
        )

        sourceTableParam = arcpy.Parameter(
            name="Source_Table",
            displayName="Source Table",
            direction=inputDirection,
            datatype="GPTableView",
            parameterType=reqParamType
        )

        fieldMatchingParam = arcpy.Parameter(
            name="Field_Matching",
            displayName="Field Matching",
            direction=inputDirection,
            datatype="GPValueTable",
            parameterType=reqParamType
        )

        fieldMatchingParam.columns=[["String", "Source Table"],["String","Target Feature Class"]]
        fieldMatchingParam.filters[0].list = []
        fieldMatchingParam.filters[0].type = "Value List"
        fieldMatchingParam.filters[1].list = []
        fieldMatchingParam.filters[1].type = "Value List"

        params = [targetFCParam,sourceTableParam,fieldMatchingParam]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        if parameters[0].altered:
            parameters[2].filters[0].list = [field.name for field in arcpy.Describe(parameters[1]).fields]
        if parameters[1].altered:
            parameters[2].filters[1].list = [field.name for field in arcpy.Describe(parameters[0]).fields]
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        targetFC = parameters[0].valueAsText
        inputTable = parameters[1].valueAsText
        fieldMatching = parameters[2].value

        arcpy.AddMessage(fieldMatching)
        arcpy.AddMessage(type(fieldMatching[0]))

        # Create a two lists. One for the Source and the other for the Target field names the user provided
        fieldNamesInput = []
        fieldNamesTarget = []
        for pair in fieldMatching:
            fieldNamesInput.append(pair[0])
            fieldNamesTarget.append(pair[1])
            

        # Now evaluate the list of user input, and just extract the field objects if the field.name was provided by the user
        fieldMapDict = {}
        fieldNamesTargetList = []
        fieldNamesInputList = []

        for field in arcpy.Describe(targetFC).fields:
            if field.name in fieldNamesTarget:
                fieldNamesTargetList.append(field)

        fieldMapDict[targetFC]=fieldNamesTargetList

        for field in arcpy.Describe(inputTable).fields:
            if field.name in fieldNamesInput:
                fieldNamesInputList.append(field)

        arcpy.AddMessage(fieldNamesTargetList)
        arcpy.AddMessage(fieldNamesInputList)

        fieldMapDict[inputTable]=fieldNamesInputList

        matchFields = ""
        fieldMaps = []

        arcpy.AddMessage(fieldMapDict)

        for i in range(len(fieldNamesTarget)): # length of the list of field names for target fc (or input)
            # Get the paired fields
            targetField = fieldMapDict[targetFC][i] # Get a field from the target FC
            inField = fieldMapDict[inputTable][i] # Get a field from the input table
            arcpy.AddMessage(inField.name + " " + targetField.name) # Print the fields being added to a field map
            # Create the empty FieldMap object
            fm = arcpy.FieldMap() # create empty field map
            # Add the input and target dataset's paired fields
            fm.addInputField(targetFC, targetField.name) # Add the target field to field map
            fm.addInputField(inputTable, inField.name) # Add the input table field to field map
            # Add the FieldMap to the list of field maps
            fieldMaps.append(fm) # append field map to the list
            # Format a string to satisfy the append tool's match_field parameter
            match = f"{fm.getInputFieldName(0)} {fm.getInputFieldName(1)};" 
            matchFields += match

        matchFields = matchFields[:-1] # Remove the last character ";"....it's not needed
        # Create the FieldMappings object
        fms = arcpy.FieldMappings()
        # Add each FieldMap to the FieldMappings object
        for fieldMap in fieldMaps:
            fms.addFieldMap(fieldMap)

        arcpy.AddMessage(f"There are {len(fieldMaps)} FieldMaps created:")
        arcpy.AddMessage(matchFields)

        arcpy.management.Append(
            inputs=inputTable,
            target=targetFC,
            schema_type="NO_TEST",
            field_mapping=fms,
            subtype="",
            expression="",
            match_fields=matchFields,
            update_geometry="NOT_UPDATE_GEOMETRY"
        )
        arcpy.AddMessage("Process complete")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
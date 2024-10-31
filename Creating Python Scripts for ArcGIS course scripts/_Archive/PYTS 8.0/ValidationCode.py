class ToolValidator:
    # Class to add custom behavior and properties to the tool and tool parameters.

    def __init__(self):
        # set self.params for use in other function
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        # Customize parameter properties.
        # This gets called when the tool is opened.
        return

    def updateParameters(self):
        # Modify parameter values and properties.
        # This gets called each time a parameter is modified, before
        # standard validation.
        mapName = arcpy.mp.ArcGISProject('current').listMaps()[0]
        self.params[0].value = mapName.name
        return

    def updateMessages(self):
        # Customize messages for the parameters.
        # This gets called after standard validation.
        if self.params[2].altered:
            xyCount = arcpy.GetCount_management(self.params[2].value)
            if int(xyCount[0]) == 0:
                self.params[2].setErrorMessage("This has no data in the rows! Call Sydney or Amanda. Or use a different input.")

        return

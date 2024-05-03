import arcpy


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
        p0 = self.params[0]
        p4 = self.params[4]
        
        if p0.altered:
            fieldNames = []
            for fld in arcpy.da.Describe(p0.value)['fields']:
                fieldNames.append(fld.name)

            p4.filter.list = fieldNames

            for fld in fieldList:
                if "Radius" in fld:
                    p4.value = fld 
        return

    def updateMessages(self):
        # Customize messages for the parameters.
        # This gets called after standard validation.
        if self.params[4].altered:
            fc = self.params[0].value
            nullCount = 0
            with arcpy.da.SearchCursor(fc, str(self.params[4].value)) as src:
                for row in src:
                    if type(row[0]) == type(None):
                        nullCount += 1
                    else:
                        pass
            del src
            if nullCount > 0:
                self.params[4].setWarningMessage(f"Your data contains {nullCount} Null values in this field. \nYou may not generate a buffer for each tree.")
        else:
            pass
        return

    # def isLicensed(self):
    #     # set tool isLicensed.
    # return True

    # def postExecute(self):
    #     # This method takes place after outputs are processed and
    #     # added to the display.
    # return
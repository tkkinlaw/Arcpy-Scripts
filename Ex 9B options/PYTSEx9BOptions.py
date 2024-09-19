# This is what's in the workbook
class ToolValidator:
    def updateMessages(self):
        # Modify the messages created by internal validation for each tool
        # parameter. This method is called after internal validation.
        if self.params[0].altered:
            if arcpy.da.Describe(self.params[0].value)["extension"] != "csv":
                self.params[0].setErrorMessage("Input table must be a CSV file")
            elif arcpy.da.Describe(self.params[0].value["extension"] == "csv":
                out_csv_file = self.params[0].value
                count = arcpy.management.GetCount(out_csv_file)
                if int(count[0]) == 0:
                    self.params[0].setErrorMessage("File contains no rows, process will likely fail")
                elif int(count[0]) > 40:
                    self.params[0].setWarningMessage(f"File has {count[0]} rows and may take an extended amount of time to process")
            else:
                pass
        return

# This is a work around that variablizes the parameter being used, reducing the length of prblematic lines in the workbook
class ToolValidator:
    def updateMessages(self):
        # Modify the messages created by internal validation for each tool
        # parameter. This method is called after internal validation.
        p0 = self.params[0]
        if self.params[0].altered:
            if arcpy.da.Describe(p0.value)["extension"] != "csv":
                p0.setErrorMessage("Input table must be a CSV file")
            elif arcpy.da.Describe(p0.value["extension"] == "csv":
                out_csv_file = p0.value
                count = arcpy.management.GetCount(out_csv_file)
                if int(count[0]) == 0:
                    p0.setErrorMessage("File contains no rows, process will likely fail")
                elif int(count[0]) > 40:
                    p0.setWarningMessage(f"File has {count[0]} rows and may take an extended amount of time to process")
            else:
                pass
        return

# A work around using more variables
class ToolValidator:
    def updateMessages(self):
        # Modify the messages created by internal validation for each tool
        # parameter. This method is called after internal validation.
        p0 = self.params[0]
        p0Ext = arcpy.da.Describe(p0.value)["extension"]
        if self.params[0].altered:
            if p0Ext != "csv":
                p0.setErrorMessage("Input table must be a CSV file")
            elif p0Ext == "csv":
                out_csv_file = p0.value
                count = arcpy.management.GetCount(out_csv_file)
                if int(count[0]) == 0:
                    p0.setErrorMessage("File contains no rows, process will likely fail")
                elif int(count[0]) > 40:
                    p0.setWarningMessage(f"File has {count[0]}, process will take longer")
            else:
                pass
        return
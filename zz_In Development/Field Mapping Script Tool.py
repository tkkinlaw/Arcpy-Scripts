import arcpy

targetFC = arcpy.GetParameterAsText(0)
inputTable = arcpy.GetParameterAsText(1)
fieldMatching = arcpy.GetParameter(2)

# Create a two lists. One for the Source and the other for the Target field names the user provided
fieldNamesInput = []
fieldNamesTarget = []
for pair in fieldMatching.exportToString().split(";"): # The arcpy.GetParameter returns a ValueTable object. This behaves differently in a Python Script tool VS Python Toolbox. 
    fieldNamesInput.append(pair.split(" ")[0])
    fieldNamesTarget.append(pair.split(" ")[1])
    

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
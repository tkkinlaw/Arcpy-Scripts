# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: This script demonstrates how to create a new spatial map series
#          CIM object used author a new map series on a layout.
# Notes:   - The script is intended to work from a script tool provided with
#            a sample project using "CURRENT".  To see the changes happen be
#            sure to active the appropriate map or layout.
#          - When running this from a script tool using CURRENT, the first time
#            the CIM gets set back to the layout, the Contents pane does not
#            refresh. Getting and resetting the Layout's CIM definition a second
#            time causes a refresh to the ribbon and the Map Series pages pane.
#          - You don't need to do this a second time if running a stand-alone
#            script.

# Parameters from user
lytName = arcpy.GetParameterAsText(0) # We can only return the name of the layout as a string.
m_name = arcpy.GetParameterAsText(1) # List the map that with the layer to process
l_name = arcpy.GetParameterAsText(2) # List the layer to process

p = arcpy.mp.ArcGISProject('current')
m = p.listMaps(m_name)[0]
l = m.listLayers(l_name)[0]

l_cim = l.getDefinition('V3')         #Get layer's CIM / Layer URI
lURI = l_cim.uRI                      #Needed to specific the index layer 
arcpy.AddMessage(lURI)

lyt = p.listLayouts(lytName)[0] # This wants a layout object.
lyt_cim = lyt.getDefinition('V3')     #Get Layout's CIM definition

#Create CIM Spatial Map Series Object and populate its properties
ms = arcpy.cim.CreateCIMObjectFromClassName('CIMSpatialMapSeries', 'V3')
ms.enabled = True
ms.mapFrameName = f"{m_name}_MF" # Name the map frame after the map processed
arcpy.AddMessage(ms.mapFrameName)
ms.startingPageNumber = 1
ms.currentPageID = 2
ms.indexLayerURI = lURI               #Index layer URI from Layer's CIM 
ms.nameField = "STATE_NAME"
ms.sortField = "STATE_NAME"
ms.sortAscending = True
ms.scaleRounding = 1000
ms.extentOptions = "BestFit"
ms.marginType = "Percent"
ms.margin = 10

lyt_cim.mapSeries = ms                #Set new map series to layout

lyt.setDefinition(lyt_cim)            #Set the Layout's CIM definition

#Force a refresh of the layout and its associated panes
lyt_cim = lyt.getDefinition('V3')
lyt.setDefinition(lyt_cim)

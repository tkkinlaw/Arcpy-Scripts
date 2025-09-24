import requests
import json
import pandas as pd
import os
import time
from arcgis import GIS
import arcgis
import datetime

# Declare parameters
date = arcpy.GetParameter(0).strftime("%Y-%m-%d")
targetGDB = arcpy.GetParameterAsText(1)
inputLyr = arcpy.GetParameter(2)

gis = GIS('Home')

layerSrc = arcpy.da.SearchCursor(inputLyr, "STATION_ID")
listNames = ','.join([row[0] for row in layerSrc])
del layerSrc
print(listNames)

arcpy.AddMessage(f"Acquiring data for {date}")

r = requests.get('https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=PRCP&stationid=' + listNames + '&startdate=' + date + '&enddate=' + date + '', headers={'token':"VuErdRKUcmflRtQQoDtKcetOXataWGfD"})
j = json.dumps(r.json()['results'], indent=5)
df = pd.read_json(j).drop(['attributes'],axis=1)

arcpy.AddMessage(f"You are working with {len(df['station'].unique())} weather stations")

df.drop(df.loc[df['datatype']!="PRCP"].index, inplace=True)
df['value_inches'] = round(df['value']/25.4, 5)
df.drop(columns='value', inplace=True)
arcpy.AddMessage(df.head(5))

arcpy.AddMessage("Data acquired")

src = arcpy.da.SearchCursor(inputLyr, "Station_ID")

stationList = []
for row in src:
    stationName = row[0][6:]
    stationList.append(stationName)

with arcpy.EnvManager(addOutputsToMap = False, workspace = targetGDB):
    for station in stationList:
        newTable = os.path.join(targetGDB, station)
        if arcpy.Exists(station):
            pass
        else:
            arcpy.management.CreateTable(targetGDB, station)
            arcpy.management.AddFields(newTable, [["Precipitation", "FLOAT", "Precipitation (inches)"], ["Date", "DATE"]])
arcpy.AddMessage("Tables for weather stations verified")

start = time.time()
for s, v, d in zip(df['station'], df['value_inches'], df['date']):
    for station in stationList:
        if station in s:
            targetTable = os.path.join(targetGDB, station)
            iCur = arcpy.da.InsertCursor(targetTable, ["Precipitation", "Date"])
            iCur.insertRow([v, d])
            del iCur
end = time.time()
arcpy.AddMessage(f"Adding the records to each table took: {round(end-start, 5)} seconds")

arcpy.env.workspace = targetGDB

allTablesList = arcpy.ListTables()
tablesList = list(set(allTablesList).intersection(stationList))

updatesMade = 0

sFieldsList=[]
[sFieldsList.append(field.name) for field in arcpy.ListFields(tablesList[0]) if field.type != "OID" ]

uFieldsList=['station_id', 'recentprcpinches']

edit = arcpy.da.Editor(arcpy.Describe(inputLyr).path)
edit.startEditing(with_undo=False, multiuser_mode=True)
edit.startOperation()

uCur = arcpy.da.UpdateCursor(inputLyr, uFieldsList)

for uRow in uCur:
    for station in tablesList:
        if uRow[0][6:] == station:
            srcTable = arcpy.da.SearchCursor(station, sFieldsList)
            for sRow in srcTable:
                updatesMade+=1
                uRow[1] = round(sRow[0], 3)
                uCur.updateRow(uRow)
            del srcTable
del uCur

edit.stopOperation()
edit.stopEditing(save_changes=True)

arcpy.AddMessage(f"There were {updatesMade} stations updated. \nDone")

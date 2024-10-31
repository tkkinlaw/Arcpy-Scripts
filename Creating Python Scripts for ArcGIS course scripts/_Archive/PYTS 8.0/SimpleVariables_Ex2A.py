# coding: utf-8
output = r"C:\EsriTraining\PYTS\Default.gdb\AffectedAreaAppCurrent"
area = r"C:\EsriTraining\PYTS\Default.gdb\AffectedArea"
distance = "0.5 Miles"
arcpy.management.CopyFeatures("AffectedAreaApp", output)
# <Result 'C:\\EsriTraining\\PYTS\\Default.gdb\\AffectedAreaAppCurrent'>
arcpy.analysis.Buffer(output, area, distance, "FULL", "ROUND", "ALL", None, "PLANAR")
# <Result 'C:\\EsriTraining\\PYTS\\Default.gdb\\AffectedArea'>

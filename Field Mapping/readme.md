## What are these files about?
In one class we were all interested in creating a python script, then a python script tool, and lastly evolving that in to a python toolbox. This tool allows the end user to update a feature class using data from a table. The tricky part of this is mapping the source table's fields to the target fields in the feature class. 

The three notebooks in this directory walk through the basics of using the arcpy.FieldMap and FieldMappings classes. Then, the Field Script Tool.py is the final python script used to create a working python toolbox (FieldMapping.atbx).

The FieldMapping.atbx contains two script tools in it, with embedded scripts in each. The first shows the first successful attempt, however the user interface is not ideal. The second script tool in the toolbox shows the completed, ideal, user interface.

Lastly, the Python Toolbox (Python Toolbox\Field Mapping.pyt) shows the same final script, but in this single-file approach of creating a elf-made geoprocessing tool.
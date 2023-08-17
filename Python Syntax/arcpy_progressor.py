import arcpy

# Define total number of steps in your task
total_steps = 10000

# Enable the Progress Dialog with default settings
arcpy.SetProgressor("default", "Processing...", 0, total_steps)

# Simulate some task that takes time for each step (replace with your own code)
for i in range(total_steps):
    # Perform some task here...

    # Update the current step of the Progress Dialog
    arcpy.SetProgressorPosition(i + 1)

# Reset/Clear the Progress Dialog once completed
arcpy.ResetProgressor()
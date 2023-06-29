import pandas as pd
import itertools
import arcgis

# Assuming your dataframe is named "df"
fc = r"C:\Demos\PYTS\ViablePops.gdb\RareSpecies_SpatialJoin"
df = pd.DataFrame.spatial.from_featureclass(fc)

# Apply custom ranking to the dataframe
orderViableDF = pd.DataFrame({'Viability':['A','B','E','C','D','F','X','H']})
sort = orderViableDF.reset_index().set_index('Viability')
df['V_Num'] = df['Viability'].map(sort['index'])

# Group the dataframe by "Species" and "EPAREGION" columns
grouped = df.groupby(["Species", "EPAREGION"])

# Create an empty list to store the rows containing the smallest combination of values
smallest_rows = []

# Iterate over each group
for group_name, group_df in grouped:
    # Extract the "V_Num" values for the group
    v_nums = group_df["V_Num"].tolist()

    # Find all possible combinations of two numbers from the group
    combinations = list(itertools.combinations(v_nums, 2))

    # Check if combinations list is empty
    if not combinations:
        continue  # Skip to the next group if no combinations are found

    # Find the smallest combination of values
    smallest_combination = min(combinations, key=sum)

    # Check if the group has only one value
    if len(v_nums) == 1:
        # If there is only one value, set it as the smallest combination itself
        smallest_combination = (v_nums[0], v_nums[0])

    # Find the rows containing the smallest combination of values
    rows = group_df[group_df["V_Num"].isin(smallest_combination)]

    # Append the rows to the list
    smallest_rows.extend(rows.values.tolist())

# Convert the list of rows to a dataframe
result_df = pd.DataFrame(smallest_rows, columns=df.columns)

print(result_df)


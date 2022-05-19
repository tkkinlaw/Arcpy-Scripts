myList = ["Coffee", "Green tea", "black tea", "herbal tea", "sparkling water", "water"]
print("Here is the original list:", myList)

# Add an item to a list
myList.append("kombucha")
print("Here is the extended list:", myList)

# Sort the list in alphabetical order (or numerical if working with integers/floats
myList.sort()
print("Here is the sorted list:", myList)

# Count the number of times a value occurs in a list
print("'water' occurs", myList.count("water"), "time(s)")

# But, it's an exact match. "water" occurs once.
# But, the string characters constituting  "water" occurs in "sparkling water" too. Here's how to count that:
print("Which elements in the item contain the characters constituting 'water'?")
i = 0
for beverage in myList:
    if "water" in beverage:
        i += 1
        print(beverage)
print("There are", i, "items in the list containing the characters constituting 'water'")
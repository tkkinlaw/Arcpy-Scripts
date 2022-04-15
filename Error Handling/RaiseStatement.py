#This script uses a raise statement to catch a specific potential error.

class DataType(Exception):
    pass

x = 10
y = "5"
try:
    if not type(x) is int:
        raise DataType
    if not type(y) is int:
        raise DataType

except DataType:
    print("One of your inputs is wrong. Only integers are allowed")

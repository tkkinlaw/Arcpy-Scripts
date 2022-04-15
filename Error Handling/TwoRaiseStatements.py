#This script uses two raise statements to catch two specific potential errors.
#Remember, Python will only raise one statement at a time. 
class DataTypeX(Exception):
    pass
class DataTypeY(Exception):
    pass
x = '10'
y = "5"
try:
    if not type(x) is int:
        raise DataTypeX
    if not type(y) is int:
        raise DataTypeY

except DataTypeX:
    print("X value is wrong. Only integers are allowed")
except DataTypeY:
    print("Y value is wrong. Only integers are allowed")

# SDJ ToolBox
A simple collection of tools fort Python
## BOOLEANS
Contains several boolean functions
- `is_int()` checks if a string can be converted in an integer or not
- `is_float()` checks if a string can be converted in a float or not
- `is_numeric()` checks if a string is a numerical expression or not

Example:
```Python
from sdj_toolbox.booleans import is_int

age = input("Enter your age: ")

if not is_int(age):
    print("That was not a correct input")
```
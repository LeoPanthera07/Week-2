| Question At Hand | Expected Solution | Actual Solution|
|-|-|-|
| print(type(True)) | bool  | bool|
| print(isinstance(True, int)) | True | True|
| print(True + True + False) | True | ==2==|
| print(int(3.99)) | 3 | 3|
| print(bool("False")) | True | True|
| print(bool("")) | False | False|
| print(0.1 + 0.2 == 0.3) | True | ==False==|
| print("5" + "3") | "53" | 53|
| print(5 + 3) | 8 | 8|


# BUGGY CODE
```name = input("Name: ")
age = input("Age: ")

if age >= 18:          # can't compare int with str
    status = "Adult"
else:
    status = "Minor"

print(f"name is {age} years old and is a {status}")   # {name}
print(f"In 5 years: {age + 5}")                       # can't perform addition  on str and int
score = 85.5
print(f"Score: {score:.0}")                            # missing f 
```

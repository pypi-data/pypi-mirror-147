import json

from . import dictionary_tools

#load a json file to dict or object
def load(filename, object = True):
    """
# load
For opening and loading a json file to dictionary or marvmiloTools.DictObj
## Example:
.  

├── example.json  

└── script.py   
### example.json:
```
{
    "hello": "world"
}
```
### script.py:
```
import marvmiloTools as mmt

dictionary = mmt.json.load("example.json", object=False)
DictObj = mmt.json.load("example.json")

print("Dictionary:")
print(dictionary)
print(type(dictionary))
print()
print("DictObject:")
print(DictObj)
print(type(DictObj))
```
### Execute like this:
```
~$ python script.py
```
### Output:
```
Dictionary:
{'hello': 'world'}
<class 'dict'>

DictObject:
{'hello': 'world'}
<class 'marvmiloTools.dictionary_tools.DictObject'>
``` 
    """
    with open(filename, "rb") as rd:
        loaded = json.loads(rd.read())
    if object:
        return dictionary_tools.toObj(loaded)
    else:
        return loaded

#save json file from dictionary to file
def save(dictionary, filename):
    """
# save
For saving a dictionary or marvmiloTools.DictObject to a json file.
## Example:
```
import marvmiloTools as mmt

dictionary = {"hello": "world"}
DictObj = mmt.dictionary.toObj(dictionary)

#save to json
mmt.json.save(dictionary, filename = "dictionary.json")
mmt.json.save(DictObj, filename = "DictObj.json")
```
### Output as dictionary.json and DictObj.json:
```
{
    "hello": "world"
}
```
    """
    with open(filename, "w") as wd:
        if type(dictionary) == dictionary_tools.DictObject:
            wd.write(json.dumps(dictionary.toDict(), indent = 4))
        else:
            wd.write(json.dumps(dictionary, indent = 4))

#write a variable to json
def write(value, json_file, path):
    """
# write
For writing a value directly to a json file without opening and saving.
## Example:
. 
 
├── example.json  

└── script.py   
### example.json:
```
{
    "dictionary": {
        "hello": "world"
    },
    "list": [
        "a",
        "b",
        "c"
    ]
}
```
### script.py:
```
import marvmiloTools as mmt

mmt.json.write("value", "example.json", ["dictionary", "new"])
mmt.json.write("new", "example.json", ["list", 1])
```
### Output example.json:
```
{
    "dictionary": {
        "hello": "world",
        "new": "value"
    },
    "list": [
        "a",
        "new",
        "b",
        "c"
    ]
}
```
    """
    json_content = load(json_file, object=False)
    current_content = json_content
    for path_val in path:
        if not path_val == path[-1]:
            try:
                current_content = current_content[path_val]
            except:
                raise KeyError("invalid path list")
        else:
            if isinstance(path_val, int):
                current_content.insert(path_val, value)
            else:
                current_content[path_val] = value
    save(json_content, json_file)
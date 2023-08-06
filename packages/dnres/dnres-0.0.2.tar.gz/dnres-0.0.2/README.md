# dnres: data n results

`dnres` is a python package for managing and sharing data and results generated from any type of data analysis. It facilitates modular type of analysis by allowing easy storing and loading of python objects or files.

## Simple implementation

First create a configuration file. Example `config.ini`:
```
[STRUCTURE]
dir1 = foo/bar
dir2 = foo/foo/bar

[DATABASE]
filename = data.db

[INFO]
description = "This is the description of the analysis related to the data and results."
```

During analysis, python objects can be stored in order to be used in another analytical script. Example `script_01.py`:
```
from dnres import DnRes

res = DnRes('config.ini')

# Create some data
x = [1,2,3]
# Store data to use in another analytical script
res.store(data=x,
          directory='dir1',
          filename='x_var.json',
          description='List with three numbers',
          source='script_01.py',
          serialization='json'
         )
```

Load stored data from `script_01.py` in `script_02.py`:
```
from dnres import DnRes

res = DnRes('config.ini')

# See stored data
print(res)

# Load stored data
x = res.load('dir1', 'x_var.json')
```

## Documentation

Detailed documentation is under development.

## License

BSD 3


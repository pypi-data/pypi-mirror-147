
# Directory Formula
A small demo library for setting proprietary Directory and formulas

### Installation
```
pip3 install DirectoryFormulas

or 

pip3 DirectoryFormulas -upgrade
```

### Get started
Get your Directory:

```Python
from DirectoryFormulas import DirX

# Changes to local if /Users/[Name]
DirX.Terminal2Local()

#Choose between Users
DirX.Directory()

#Choose between destination
DirX.Directory_Local()
DirX.Directory_Cloud()

DirX.FileOrder(Mininbars) # integer needed
# Fldict = {1:'-A-',5:'-B-',10:'-C-',15:'-D-',30:'-E-'}

#Avoid Error
DirX.DivByZero_int(a,b)
DirX.DivByZero_float(a,b)

#Save .csv from .parquet as a slice
DirX.RunCSV_Saver(fromdate, DirectoryTrigger)
```

```Python
Functions_OPT(DirX)
    Statistics_OPT
```
# SpatialQuadTree

## How to run
### Compile
```
g++ main.cpp QuadTree.cpp Input.cpp -o quadTree
```

### Generating Queries
```
python3 data_query_generator.py -xl=-500 -yl=-200 -xh=500 -yh=200
 -n=100000
```
Parameters:
- `-xl` - X-Low for boundary (Bottom Left), default = -180
- `-yl` - Y-Low for boundary (Bottom Left), default = -90

- `-xh` - X-High for boundary (Top Right), default = 180
- `-yh` - Y-High for boundary (Top Right), default = 90

- `-n` - Number of total queries to generate, default = 100000
- `-s` - Sortedness (Fraction of queries that follow path), default = 0.6 - 60% of queries follow path, rest are randomly generated

### Execute 


#### (Linux)
```
.\quadTree dataExample.txt -1 queryExample.txt 1
```
#### (Windows)
```
.\quadTree.exe dataExample.txt -1 queryExample.txt {mode}
```

mode can be:
- 0: naive bulk insert
- 1: bulk insert with optimization 1
- n or leave empty: normal

-1 means load all data from dataExample.txt

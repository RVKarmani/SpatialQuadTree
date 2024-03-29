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

- `-n` - Number of total queries to generate, default = 1000000
- `-s` - Sortedness (Fraction of queries that follow path), default = 0.6 - 60% of queries follow path, rest are randomly generated

### Execute 


#### (Linux)
```
./quadTree.out dataExample.txt -1 queryExample.txt {mode}
```
#### (Windows)
```
.\quadTree.exe dataExample.txt -1 queryExample.txt {mode}
./quadTree dataExample.txt -1 queryExample.txt b
```

mode can be:
- i: naive insert
- b: bulk insert
- n or leave empty: normal

-1 means load all data from dataExample.txt

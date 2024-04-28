# SpatialQuadTree

## How to run
### Compile
```
g++ main.cpp QuadTree.cpp Input.cpp -o quadTree
```
### Execute 
```
./quadTree [init_data_file] -1 [insert_data_file] [mode] [level]
```
[mode] can be:
- 0: naive bulk insert
- 1: bulk insert with optimization 1
- n or leave empty: normal
  
[level] can be:
- 0, 1, 2, ... represent level of parent stored during optimized bulk insert

-1 means load all data from dataExample.txt
#### (Linux)
```
./quadTree dataExample.txt -1 queryExample.txt 1
```
#### (Windows)
```
.\quadTree.exe ./data/empty.txt -1 ./data/s/insert_s=0.75.txt 1 0
```

## Generating Queries
```
python3 data_query_generator.py -xl=-500 -yl=-200 -xh=500 -yh=200 -n=100000
```
or
```
python data_query_generator.py -n=100000 -s 0
```

Parameters:
- `-xl` - X-Low for boundary (Bottom Left), default = -180
- `-yl` - Y-Low for boundary (Bottom Left), default = -90

- `-xh` - X-High for boundary (Top Right), default = 180
- `-yh` - Y-High for boundary (Top Right), default = 90

- `-n` - Number of total queries to generate, default = 100000
- `-s` - Sortedness (Fraction of queries that follow path), default = 0.6 - 60% of queries follow path, rest are randomly generated
- `-c` - Curve type for data, random_curve, fermat_spiral, circ_arc, bezier

## Visualize insert file
```
python visualization.py -f="insert.txt"
```


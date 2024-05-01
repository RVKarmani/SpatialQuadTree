#!/bin/bash
python3 data_query_generator.py -s 0.0 -c bezier -n 1000000 -d gaussian
python3 data_query_generator.py -s 0.25 -c bezier -n 1000000 -d gaussian
python3 data_query_generator.py -s 0.5 -c bezier -n 1000000 -d gaussian
python3 data_query_generator.py -s 0.75 -c bezier -n 1000000 -d gaussian
python3 data_query_generator.py -s 1.0 -c bezier -n 1000000 -d gaussian

python3 data_query_generator.py -s 0.75 -c fermat_spiral -n 100000 -d gaussian
python3 data_query_generator.py -s 0.75 -c fermat_spiral -n 1000000 -d gaussian
python3 data_query_generator.py -s 0.75 -c fermat_spiral -n 10000000 -d gaussian
python3 data_query_generator.py -s 0.75 -c fermat_spiral -n 100000000 -d gaussian

python3 data_query_generator.py -s 0.75 -c fermat_spiral -n 100000 -d uniform
python3 data_query_generator.py -s 0.75 -c fermat_spiral -n 1000000 -d uniform
python3 data_query_generator.py -s 0.75 -c fermat_spiral -n 10000000 -d uniform
python3 data_query_generator.py -s 0.75 -c fermat_spiral -n 100000000 -d uniform
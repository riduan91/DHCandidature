#!/bin/bash
nb_line=`fgrep -o \",\" ../Data/source_file.csv | wc -l`
python Run.py ../Data/source_file.csv 1 $((nb_line/103))

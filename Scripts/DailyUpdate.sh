#!/bin/bash
nb_line_FR=`fgrep -o \",\" ../Data/source_file_FR.csv | wc -l`
nb_line_SG=`fgrep -o \",\" ../Data/source_file_SG.csv | wc -l`
nb_line_TW=`fgrep -o \",\" ../Data/source_file_TW.csv | wc -l`

nb_col_FR=103
nb_col_SG=104
nb_col_TW=103

python Run.py ../Data/source_file_FR.csv 1 $((nb_line_FR/nb_col_FR))
python Run.py ../Data/source_file_SG.csv 1 $((nb_line_SG/nb_col_SG))
python Run.py ../Data/source_file_TW.csv 1 $((nb_line_TW/nb_col_TW))


#!/bin/bash

Schools="BKHN TNHN XD GTVT1 VINH BKDN KTDN SPDN NNDN DALAT BKHCM TNHCM GTVT2 KHAC"
Folders="../Docs/"
Interview_Folders="../Docs/INTERVIEW/"

for school in $Schools
do
	rm -r $Folders$school/*
	rm -r $Interview_Folders$school/*
done

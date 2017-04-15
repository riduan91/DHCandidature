#!/bin/bash

Schools="KTLHCM CNHN"
Folders="../Docs/"
Interview_Folders="../Docs/INTERVIEW/"

for school in $Schools
do
	echo "Removing $school" 
	rm -r $Folders$school/*
	rm -r $Interview_Folders$school/*
done

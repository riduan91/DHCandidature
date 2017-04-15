#!/bin/bash

Schools="CTHO"
Folders="../Docs/"
Interview_Folders="../Docs/INTERVIEW/"

for school in $Schools
do
	rm -r $Folders$school/*
	rm -r $Interview_Folders$school/*
done

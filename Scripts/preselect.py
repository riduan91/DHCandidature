# !/user/local/bin/python2.7
# -*- coding: utf-8 -*-

import os, sys, csv

def transformCSVToList(filename):
    with open(os.path.abspath(filename), 'rU') as f:
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter = ','))
        f.close()
    return data

def preselect(data):
    newdata = []
    for line in data:
        if line[-1]!='' and line[-1]!=' ' and line[-1]!='0':
            line[-1]=''
            newdata.append(line)
    return newdata

if __name__ == '__main__':
    data = transformCSVToList(sys.argv[1])
    newdata = preselect(data)
    myfile = open(sys.argv[1][:-15] + "_Preselected.csv", 'w')
    for i in xrange(len(newdata)):
        for j in range(1, len(newdata[0])):
            myfile.write(",")
            myfile.write(str(newdata[i][j]))
        myfile.write("\n")
    myfile.close()
    print "Successfully finished."
            

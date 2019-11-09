#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Created on Wed Apr 18 14:58:23 2018 @File: strip_blank.py @author: lidongchao """

import sys, csv

contents = []
with open(sys.argv[1]) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        contents.append([x.strip() for x in row])
for content in contents:
    print(','.join(content)) 

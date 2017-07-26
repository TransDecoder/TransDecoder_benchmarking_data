#!/usr/bin/env python

import os
import sys
import re

# usage:  find . -regex ".*prodigal.out" |  extract_prodigal_+.py
#    it extracts the '+' strand records and outputs them to the filename.+only

files = sys.stdin.readlines()
for file in files:
    file = file.rstrip()
    plus_only_file = file + ".+only"
    ofh = open(plus_only_file, 'w')

    with open(file) as fh:
        for line in fh:
            if not re.search("^\#", line):
                x = line.split("\t")
                if x[6] == '+':
                    ofh.write(line)
    ofh.close()
    sys.stderr.write("-wrote {}\n".format(plus_only_file))


sys.exit(0)


    
    

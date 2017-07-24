#!/usr/bin/env python

import sys

usage = "usage: {} input.gff > output.cds.gff\n\n".format(sys.argv[0])
if len(sys.argv) < 2:
    sys.stderr.write(usage)
    sys.exit(1)

input_gff = sys.argv[1]

f_pred = open(input_gff)
#write CDS prediction to an output file
predictions = f_pred.readlines()
for pred in predictions:
    if '\tCDS\t' in pred:
        sys.stdout.write(pred)


sys.exit(0)





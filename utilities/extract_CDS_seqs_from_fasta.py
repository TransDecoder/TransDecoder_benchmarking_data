#!/usr/bin/env python

#creates random fragments from a list of transcripts
import numpy as np
import os,sys,argparse
from random import randint
import random
path = os.getcwd()


usage = "usage: {} target.fasta\n\n".format(sys.argv[0])

if len(sys.argv) < 2:
    sys.stderr.write(usage)
    sys.exit(1)



in_file = sys.argv[1]

f = open(path+"/"+in_file,"r")
lines = f.readlines()


for i in range(len(lines)):
    if lines[i].startswith('>'):

        # get orf coordinates
        seq_header = lines[i]  # example: >AT3G25110-lcl_NC_003074_8_mrna_NM_113415_4_30732|CDS:1-559|length:809|
        seq_header = seq_header.rstrip()

        cds_end = int(seq_header.split('|')[1].split(':')[1].split('-')[1])
        cds_st = int(seq_header.split('|')[1].split(':')[1].split('-')[0])

        # select a breakpoint at a random position within the transcript length
        seq = lines[i+1].rstrip()

        cds_seq = seq[cds_st-1 : cds_end]

        header = seq_header[1:]
        acc = header.split("|")[0]
        
        print(">{}|{}-{} {}\n{}".format(acc, 1, len(cds_seq), header, cds_seq))


        


#!/usr/bin/env python

#creates random fragments from a list of transcripts
import numpy as np
import os,sys,argparse
from random import randint
import random
path = os.getcwd()

in_file = sys.argv[1]
op_file = sys.argv[2]
f = open(path+"/"+in_file,"r")
fw = open(path+"/"+op_file,"w")
lines = f.readlines()

#normal distribution
mu = 0.5
sigma  = 0.1
dist = np.random.normal(mu, sigma, len(lines))

all_frag_trans = {}
for i in range(len(lines)):
    if lines[i].startswith('>'):

        # get orf coordinates
        seq_header = lines[i]  # example: >AT3G25110-lcl_NC_003074_8_mrna_NM_113415_4_30732|CDS:1-559|length:809|

        cds_end = int(seq_header.split('|')[1].split(':')[1].split('-')[1])
        cds_st = int(seq_header.split('|')[1].split(':')[1].split('-')[0])

        # select a breakpoint at a random position within the transcript length
        seq = lines[i+1].rstrip()
        chop_ratio = random.choice(dist)
        chop_pos = int( (cds_end - cds_st) * chop_ratio) + cds_st
        
        # split the sequence at the breakpoint
        frags = [seq[:chop_pos], seq[chop_pos:]]

        # take the shorter one
        f = frags[0]
        adj_cds_st = cds_st
        adj_cds_end = chop_pos

        midpt = (cds_st + cds_end) / 2
        
        if chop_pos > midpt:
            f = frags[1]
            adj_cds_st = 1
            adj_cds_end = cds_end-chop_pos
        
        frag_length = len(f)
        
        
        line = lines[i].split('|')
        key = line[0]+'|CDS:'+str(adj_cds_st)+'-'+str(adj_cds_end)+'|length:'+str(frag_length)+'|'
        all_frag_trans[key] = f



for key in all_frag_trans.keys():
    fw.write(key+'\n')
    fw.write(all_frag_trans[key]+'\n') 


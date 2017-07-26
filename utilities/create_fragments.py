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
         chop = int(len(lines[i+1])*dist[i])
         frag = [lines[i+1].strip()[:chop],lines[i+1].strip()[chop:]]
         randomindex = random.randint(0,1)
         length = len(frag[randomindex])
         f = frag[randomindex]
         cds_end = int(lines[i].split('|')[1].split(':')[1].split('-')[1])
         cds_st = int(lines[i].split('|')[1].split(':')[1].split('-')[0])
         if chop>= cds_st and chop<= cds_end:
             if randomindex == 0:
                cds_end = chop
             elif randomindex == 1:
                cds_st = 1
                cds_end = cds_end-chop
         else:
             if chop > cds_end:
                 f = lines[i+1].strip()[:chop]
                 cds_st = cds_st
                 cds_end = cds_end-1
             elif chop < cds_st:
                 f = lines[i+1].strip()[chop:]
                 cds_st = cds_st-chop+1
                 cds_end = cds_end-chop+1-1
         if cds_end<0:    
              print cds_end, cds_end,chop, lines[i]
         line = lines[i].split('|')
         key = line[0]+'|CDS:'+str(cds_st)+'-'+str(cds_end)+'|length:'+str(len(frag[randomindex]))+'|'
         all_frag_trans[key] = f

for key in all_frag_trans.keys():
    fw.write(key+'\n')
    fw.write(all_frag_trans[key]+'\n') 


#!/usr/bin/env python

import os, re, sys
import numpy as np
import collections

usage = "\n\n\tusage: {} seqs.fasta targetGCpct\n\n".format(sys.argv[0])

if len(sys.argv) < 3:
    sys.stderr.write(usage)
    sys.exit(1)


def main():
    fasta_file = sys.argv[1]
    target_gc_pct = float(sys.argv[2])

    if target_gc_pct < 1 or target_gc_pct > 100:
        sys.stderr.write("Error, targetGCpct must be between 1 and 100")
        sys.exit(2)

    

    acc = None
    seq = ''
    with open(fasta_file) as fh:
        for line in fh:
            line = line.strip()
            m = re.search('>(\S+)', line)
            if m:
                if acc:
                    mirror_seq(acc, seq, target_gc_pct)
                acc = m.group(1)
                seq = ''
            else:
                seq += line

    # get last one
    mirror_seq(acc, seq, target_gc_pct)

    sys.exit(0)

def mirror_seq(acc, seq, target_gc_pct):

    seq = seq.upper()

    print ">{}\n{}".format(acc, seq)
    
    seqlen = len(seq)
    chars = ['G', 'A', 'T', 'C']

    g_or_c = target_gc_pct / 100.0 / 2;
    a_or_t = (100-target_gc_pct) / 100.0 / 2;
    
    probs = [g_or_c, a_or_t, a_or_t, g_or_c]
    
    randseq = ''.join(np.random.choice(chars, p=probs) for _ in range(seqlen))
    
    print ">random{}-\n{}".format(acc, randseq)

    


if __name__ == '__main__':
    main()

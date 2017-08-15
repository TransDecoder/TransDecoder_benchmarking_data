#!/usr/bin/env python

import os, re, sys
import numpy as np
import collections

usage = "\n\n\tusage: {} seqs.fasta\n\n".format(sys.argv[0])

if len(sys.argv) < 2:
    sys.stderr.write(usage)
    sys.exit(1)


def main():
    fasta_file = sys.argv[1]

    acc = None
    seq = ''
    with open(fasta_file) as fh:
        for line in fh:
            line = line.strip()
            m = re.search('>(\S+)', line)
            if m:
                if acc:
                    mirror_seq(acc, seq)
                acc = m.group(1)
                seq = ''
            else:
                seq += line

    # get last one
    mirror_seq(acc, seq)
        

    sys.exit(0)

def mirror_seq(acc, seq):

    seq = seq.upper()

    print ">{}\n".format(acc, seq)
    
    seqlen = len(seq)
    charcounter = collections.defaultdict(int)
    for char in seq:
        charcounter[char] += 1

    chars = charcounter.keys()
    probs = list()
    for char in chars:
        char_count = charcounter[char]
        p = float(char_count) / seqlen
        probs.append(p)

    randseq = ''.join(np.random.choice(chars, p=probs) for _ in range(seqlen))


    print ">random{}\n{}".format(acc, randseq)

    


if __name__ == '__main__':
    main()

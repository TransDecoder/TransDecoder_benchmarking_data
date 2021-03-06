#!/usr/bin/env python

#Compares the output of an algorithm with the reference

import os,sys
import re
import argparse

path = os.getcwd()

#add options to inputs
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description="classify predictions as TP, FP, and identify FNs")
parser.add_argument("--preds", type=str, required=True, help= "CDS predictions gff")
parser.add_argument("--truth", type=str, required=True, help= "CDS truth (reference) set gff")

args = parser.parse_args()

f_truth = open(args.truth)
f_pred = open(args.preds)


truth_lines = f_truth.readlines()
prediction = f_pred.readlines()

three_match = []
three_five_match = []
false_pos = []
false_neg = []

#store all annotations

truth_predictions = {}

for line in truth_lines:
    line = line.strip()
    x = line.split("\t")

    transcript_id = x[0]

    try:
        truth_orf = { 'transcript_id' : transcript_id,
                      'ref_start' : int(x[3]),
                        'ref_end' : int(x[4]),
                      'ref_orient' : x[6],
                      'ref_length' : int(x[4]) - int(x[3]) + 1
                      }
    except:
        sys.stderr.write("Error parsing coordinate info from line: {}\n".format(line))
        continue
    
    truth_predictions[transcript_id] = truth_orf


MAX_WARN=20
num_warnings = 0
#store all predictions
transcripts_with_predictions = set()
for pred in prediction:
    
    line = pred.strip().split('\t')
    transcript_id = line[0].split('|')[0]

    transcripts_with_predictions.add(transcript_id)
    
    ref_st = -1
    ref_end = -1
    ref_orient = '?'
    ref_length = -1
    
    if transcript_id in truth_predictions:
        truth_struct = truth_predictions[transcript_id]
        ref_st = truth_struct['ref_start']
        ref_end = truth_struct['ref_end']
        ref_orient = truth_struct['ref_orient']
        ref_length = truth_struct['ref_length']
    else:
        num_warnings += 1
        if num_warnings < MAX_WARN:
            sys.stderr.write("warning, missing {} in truth set (ok if thats expected)\n".format(transcript_id))
        elif num_warnings == MAX_WARN:
            sys.stderr.write("-disabling further warning messages\n")
    
    
    pred_st = -1
    pred_end = -1

    try:
        pred_st = int(line[3])
        pred_end = int(line[4])
    except:
        sys.stderr.write("Error, cannot parse coordinate info from line: {}\n".format(pred))
        continue
    
    pred_orient = line[6]
    pred_length = pred_end - pred_st + 1
     
    result = "\t".join([transcript_id,
                        str(ref_st), str(ref_end), ref_orient, str(ref_length),
                        str(pred_st), str(pred_end), pred_orient, str(pred_length)])
     
    if (ref_orient == pred_orient
        and
        abs(ref_end - pred_end) < 3
        and
        abs(ref_st - pred_st) < 3 ) :
         
        three_five_match.append("\t".join(['TP', result, '3,5-prime']))

    elif ref_orient == pred_orient and abs(ref_end - pred_end) < 3:
        three_match.append("\t".join(['TP', result, '3-prime']))
        
    else:
        false_pos.append("\t".join(['FP', result, '.']))


#store missing predictions
no_res = list(set(truth_predictions.keys()) - transcripts_with_predictions)
for transcript_id in no_res:
    truth_struct = truth_predictions[transcript_id]

    result = "\t".join([transcript_id,
                       str(truth_struct['ref_start']), str(truth_struct['ref_end']),
                        truth_struct['ref_orient'], str(truth_struct['ref_length']),
                       '.', '.', '.', '.'])
    
    false_neg.append("\t".join(['FN', result, '.']))


# header
print("\t".join(['Status', 'transcript_id', 'ref_st', 'ref_end', 'ref_orient', 'ref_len', 
                 'pred_st', 'pred_end', 'pred_orient', 'pred_length', 'match_type']))

#write to file
def write(lst):
    for item in lst:
        print(item)        

write(three_five_match)
write(three_match)
write(false_pos)
write(false_neg)

sys.exit(0)

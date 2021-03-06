#!/usr/bin/env python

import os,sys
import re
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from sklearn.metrics import auc
import argparse
import logging

logger = logging.getLogger(__name__)

## Defining the range of prediction lengths to consider
MIN_LENGTH_RANGE = 300   # any orfs, truth or predicted, will not be considered if smaller than this amount.
max_range = 750
step_size = 30


#calculate sensitivity and specificity for a given list
def compute_accuracy_min_pred_len(lst, min_pred_len):

    preds_min_len = [ pred for pred in lst if pred['pred_length'] >= min_pred_len ] 
    
    tp = 0
    fp = 0

    TP_containing_transcripts = set()

    for pred in preds_min_len:
        transcript_id = pred['transcript_id']
        match_type = pred['match_type']
            
        result_class = pred['result_class']
        
        if result_class == "TP":
            if ( (strict_mode and re.search("5", match_type)) or not strict_mode):
                tp +=1
                TP_containing_transcripts.add(transcript_id)
        elif result_class ==  "FP":
            fp +=1
        else:
            raise RuntimeError("prediction has unrecognized result_class: {}".format(result_class))
        
        #print("\t".join([`min_pred_len`, result_class, transcript_id, match_type]))

    fn = len(truth_set_transcripts - TP_containing_transcripts)
    
    sensitivity = float(tp)/float(tp+fn)
    specificity = float(tp)/float(tp+fp)

    print("\t".join([str(x) for x in [min_pred_len, tp, fp, fn, sensitivity, specificity, 1-specificity] ]))

    
    return sensitivity, specificity




def auc(ordered_pts_list):

    pts = ordered_pts_list[:]

    auc = 0

    ptA = pts.pop(0)

    while pts:
        ptB = pts.pop(0)

        x1 = ptA[0]
        y1 = ptA[1]

        assert(x1 >= 0)
        assert(y1 >= 0)

        x2 = ptB[0]
        y2 = ptB[1]

        assert(x2 >= 0)
        assert(y2 >= 0)

        delta_x = abs(x2-x1)
        delta_y = abs(y2-y1)

        min_y = min(y1, y2)

        base_trap_area = min_y * delta_x
        top_triangle_area = delta_y * delta_x / 2

        trap_area = base_trap_area + top_triangle_area

        if x2 > x1:
            auc += trap_area
        else:
            auc -= trap_area
            
        logger.debug("auc between pts {} and {}: {}".format(ptA, ptB, trap_area))

        # set up for next pt
        ptA = ptB
    
    logger.debug("auc total area: {}".format(auc))

    return auc



#add options to inputs
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description="plot ROC ")

parser.add_argument("--pred_name", type=str, required=True, help="name for prediction method")

parser.add_argument("--scored_preds", type=str, required=True, help= "scored predictions including TP, FP, and FN")

parser.add_argument("--strict", action="store_true", default=False, help="require both start and stop codon match for TP")

args = parser.parse_args()


predictor_name = args.pred_name
scored_preds_file = args.scored_preds
strict_mode = args.strict

#plot ROC curve of an algorithm

path = os.getcwd()


#input files

f_pred = open(scored_preds_file)

prediction_text_lines = f_pred.readlines()

# remove header
prediction_text_lines = prediction_text_lines[1:] 

"""
Format:

0       Status
1       transcript_id
2       ref_st
3       ref_end
4       ref_orient
5       ref_len
6       pred_st
7       pred_end
8       pred_orient
9       pred_length
10      match_type

0       TP
1       NM_102026
2       40
3       375
4       +
5       336
6       40
7       375
8       +
9       336
10      3,5-prime

"""



truth_set_transcripts = set()

all_predictions = []

for pred in prediction_text_lines:
    pred = pred.rstrip()
    pred = pred.split('\t')

    ref_len = int(pred[5])
    if ref_len > 0 and int(ref_len) < MIN_LENGTH_RANGE:
        # ignoring reference entries that are below the minimum prediction length.
        #sys.stderr.write("skipping short ref line: {}\n".format(pred))
        continue

    
    pred_result_class = pred[0]
    transcript_id = pred[1]
    pred_start = pred[6]
    pred_end = pred[7]
    pred_orient = pred[8]
    pred_length = pred[9]
    match_type = pred[10]

    if pred_length != "." and int(pred_length) < MIN_LENGTH_RANGE:
        # ignoring all short predictions below min length
        #sys.stderr.write("skipping short pred line: {}\n".format(pred))
        continue
    

    # capture truth set
    if pred_result_class in ("TP", "FN"):
        truth_set_transcripts.add(transcript_id)


    # capture all predictions
    if pred_result_class != 'FN':
        pred_name = ":".join([transcript_id, pred_start, pred_end, pred_orient])

        pred_struct = {
            'pred_name' : pred_name,
            'pred_length' : int(pred_length),
            'match_type' : match_type,
            'transcript_id' : transcript_id,
            'result_class' : pred_result_class
            } 

        all_predictions.append(pred_struct)


predictions_sorted_by_length = sorted(all_predictions, key=lambda pred: pred['pred_length'])


print("\t".join(["min_pred_len", "TP", "FP", "FN", "Sensitivity", "Specificity", "1-Specificity"]))

#iterate through the length list with a minimum gene length criteria ranging between 90bp and 480bp with a step of 30bp

accuracy_stats = []

ranges = range(MIN_LENGTH_RANGE, max_range+1, step_size)
ranges.reverse()

for min_pred_len in ranges:

    (sensitivity, specificity) = compute_accuracy_min_pred_len(predictions_sorted_by_length, min_pred_len)

    accuracy_stats.append( { 'min_pred_len' : min_pred_len,
                             'sensitivity' : sensitivity,
                             'specificity' : specificity,
                             '1-specificity' : 1 - specificity,
                             } )


# add bounds

# This is the ROC curve
x_n = [ x['1-specificity'] for x in accuracy_stats ]
y_n = [ y['sensitivity'] for y in accuracy_stats ]



plt.plot(x_n, y_n, marker ='+')

# This is the AUC using built-in function

# add bounds
x_n = [0] + x_n + [1]
y_n = [0] + y_n + [1]


roc_auc = auc(zip(x_n, y_n))


print("#AUC = %.4f" % roc_auc) 

plt.title(predictor_name + ', AUC = %.4f' % roc_auc)

dname = os.path.dirname(scored_preds_file)
if not dname:
    dname = "."
    
pdf_plot_filename = dname + "/" + predictor_name + ".roc.pdf"

try:
    pp = PdfPages(pdf_plot_filename)
    pp.savefig(plt.gcf())
    pp.close()
    sys.stderr.write("Wrote ROC plot figure: {}\n".format(pdf_plot_filename))
except:
    pass

sys.exit(0)

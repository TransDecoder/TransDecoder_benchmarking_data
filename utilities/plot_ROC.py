#!/usr/bin/env python

import os,sys
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from sklearn.metrics import auc
import argparse


#add options to inputs
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description="plot ROC ")

parser.add_argument("--pred_name", type=str, required=True, help="name for prediction method")

parser.add_argument("--scored_preds", type=str, required=True, help= "scored predictions including TP, FP, and FN")

args = parser.parse_args()


predictor_name = args.pred_name
scored_preds_file = args.scored_preds


#plot ROC curve of an algorithm

path = os.getcwd()


#input files

f_pred = open(scored_preds_file)

predictions = f_pred.readlines()

# remove header
predictions = predictions[1:] 

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


total_truth_set = 0
len_stat = []
for pred in predictions:
    pred = pred.split('\t')
    pred_result_class = pred[0]
    if pred_result_class != 'FN':
        pred_len = int(pred[9])
        l = [pred_len, pred_result_class]
        len_stat.append(l)

    if pred_result_class in ("TP", "FN"):
        total_truth_set += 1

sorted_len_stats = sorted(len_stat)


#calculate sensitivity and specificity for a given list
def compute_accuracy_min_pred_len(lst, min_pred_len):

    preds_min_len = [ (j,k) for (j,k) in lst if j >= min_pred_len ] 
    
    tp = 0
    fp = 0

    for l in preds_min_len:
        if l[1] == "TP":
            tp +=1              
        elif l[1] ==  "FP":
            fp +=1
    fn = total_truth_set - tp
    
    sensitivity = float(tp)/float(tp+fn)
    specificity = float(tp)/float(tp+fp)

    print("\t".join([str(x) for x in [min_pred_len, tp, fp, fn, sensitivity, specificity, 1-specificity] ]))
    
    return sensitivity, specificity


print("\t".join(["min_pred_len", "TP", "FP", "FN", "Sensitivity", "Specificity", "1-Specificity"]))

#iterate through the length list with a minimum gene length criteria ranging between 90bp and 480bp with a step of 30bp

accuracy_stats = []
step_size = 30
min_range = 90
max_range = 480

ranges = range(min_range, max_range+1, step_size)
ranges.reverse()

for min_pred_len in ranges:

    (sensitivity, specificity) = compute_accuracy_min_pred_len(sorted_len_stats, min_pred_len)

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

roc_auc = auc(x_n, y_n, reorder = True)

print("#AUC = %.4f" % roc_auc) 

plt.title(predictor_name + ', AUC = %.4f' % roc_auc)

pdf_plot_filename = os.path.dirname(scored_preds_file) + "/" + predictor_name + ".roc.pdf"
pp = PdfPages(pdf_plot_filename)
pp.savefig(plt.gcf())
pp.close()
sys.stderr.write("Wrote ROC plot figure: {}\n".format(pdf_plot_filename))

sys.exit(0)

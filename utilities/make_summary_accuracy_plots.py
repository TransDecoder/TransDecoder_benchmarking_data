#!/usr/bin/env python

import os, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

usage = "\n\n\nusage: {} plot_title pred_type_A:/path/to/pred_type_A.cds.gff.scored.roc ...\n\n\n".format(sys.argv[0])

if len(sys.argv) < 2:
    sys.stderr.write(usage)
    sys.exit(1)



def main():


    pdf_plot_filename = "summary_ROC.pdf"
    pp =  PdfPages(pdf_plot_filename)

    ## roc plot summary
    plt.figure()
    title = sys.argv[1]
    plt.title(title + " : ROC")
    plt.xlabel("1-Specificity")
    plt.ylabel("Sensitivity")
    
    predtype_file_combos = sys.argv[2:]

    pred_types = []
    auc_vals = []
        
    for predtype_file_combo in predtype_file_combos:
        (pred_type, roc_file) = predtype_file_combo.split(":")

        (x_vals, y_vals, auc) = parse_roc_file(roc_file) 

        plt.plot(x_vals, y_vals, marker = 'o', label=pred_type)

        pred_types.append(pred_type)
        auc_vals.append(auc)

    plt.legend(loc="lower right")

    pp.savefig(plt.gcf())


    ## auc barplot summary
    plt.figure()
    x_pos = np.arange(len(pred_types))
    plt.bar(x_pos, auc_vals, align='center', alpha=0.5)
    plt.xticks(x_pos, pred_types)
    plt.ylabel("prediction type")
    plt.title(title + " : AUC")

    pp.savefig(plt.gcf())
    
    pp.close()
    

    sys.exit(0)
    


'''
example file content:
min_pred_len    TP      FP      FN      Sensitivity     Specificity     1-Specificity
480     25340   1637    15837   0.615392087816  0.939318678875  0.0606813211254
450     25770   2212    15407   0.625834810695  0.920949181617  0.0790508183832
420     26227   3031    14950   0.63693323943   0.896404402215  0.103595597785
390     26614   4202    14563   0.646331690021  0.863642263759  0.136357736241
360     26988   5956    14189   0.655414430386  0.81920835357   0.18079164643
330     27395   8504    13782   0.665298589018  0.76311317864   0.23688682136
300     27740   12361   13437   0.673677052724  0.69175332286   0.30824667714
270     27740   12369   13437   0.673677052724  0.691615348176  0.308384651824
240     27740   12369   13437   0.673677052724  0.691615348176  0.308384651824
210     27740   12369   13437   0.673677052724  0.691615348176  0.308384651824
180     27740   12369   13437   0.673677052724  0.691615348176  0.308384651824
150     27740   12369   13437   0.673677052724  0.691615348176  0.308384651824
120     27740   12369   13437   0.673677052724  0.691615348176  0.308384651824
90      27740   12369   13437   0.673677052724  0.691615348176  0.308384651824
#AUC = 0.7592
'''

def parse_roc_file(roc_file):
    lines = open(roc_file).readlines()

    # remove header
    lines = lines[1:]

    auc_text = lines.pop()
    auc_text = auc_text.rstrip()
    auc_val = float(auc_text.split(" ")[2])

    x_vals = []
    y_vals = []
    for line in lines:
        line = line.rstrip()
        vals = line.split("\t")

        one_minus_specificity = float(vals[6])
        sensitivity = float(vals[4])

        x_vals.append(one_minus_specificity)
        y_vals.append(sensitivity)


    return(x_vals, y_vals, auc_val)


if __name__ == '__main__':
    main()

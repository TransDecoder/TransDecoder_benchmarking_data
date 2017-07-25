#!/usr/bin/env python

import os, sys, re
import json
import subprocess

usage = "\n\nusage: {} data.json\n\n".format(sys.argv[0])

if len(sys.argv) < 2:
    sys.stderr.write(usage)
    sys.exit(1)

data_json_file = sys.argv[1]

UTILDIR = os.path.dirname(__file__)


def run_analysis_pipe(prediction_type, ref_orfs_file, predictions_result_file, analysis_output_dir):


    ## extract CDS records
    predictions_cds_gff = "{}/{}.cds.gff".format(analysis_output_dir, prediction_type)

    cmd = str(UTILDIR + "/extract_CDS_records.py " + predictions_result_file +
              " > {}".format(predictions_cds_gff) )

    subprocess.check_call(cmd, shell=True)


    ## scoring
    scored_predictions_file = predictions_cds_gff + ".scored"

    cmd = str(UTILDIR + "/score_TP_FP_FN.py " +
              " --preds {} ".format(predictions_cds_gff) +
              " --truth {}".format(ref_orfs_file) +
              " > {} ".format(scored_predictions_file) )

    subprocess.check_call(cmd, shell=True)


    ## ROC plots
    roc_data_file = scored_predictions_file + ".roc"
    
    cmd = str(UTILDIR + "/plot_ROC.py --pred_name {} ".format(prediction_type) +
              " --scored_preds {} ".format(scored_predictions_file) +
              " > {} ".format(roc_data_file) )

    subprocess.check_call(cmd, shell=True)

    
              
    

def main():

    analysis_outputdir = os.path.abspath("analysis_dir")
    if not os.path.exists(analysis_outputdir):
        os.makedirs(analysis_outputdir)


    
    jstext = "".join(open(data_json_file).readlines())

    print(jstext)

    json_struct = json.loads(str(jstext))

    data = json_struct['data']

    ref_orfs_file = data['REFERENCE']

    predictions_dict = data['PREDICTIONS']

    for prediction in predictions_dict:

        prediction_result_file = predictions_dict[prediction]['result']
        print("{} -> {}".format(prediction, prediction_result_file))

        run_analysis_pipe(prediction, ref_orfs_file, prediction_result_file, analysis_outputdir)


    sys.exit(0)



if __name__ == "__main__":
    main()

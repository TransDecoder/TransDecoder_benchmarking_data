#!/usr/bin/env python

import sys, os, re
sys.path.insert(0, os.environ['HOME'] + "/GITHUB/TransDecoder/util/misc")
import select_TD_orfs as td


def main():
    
    import argparse
    import argparse

    parser = argparse.ArgumentParser(description="transdecoder orf selection algorithm", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--long_orfs_cds", dest="long_orfs_cds_filename", type=str, default="", required=True, help="longest_orfs.cds file")
    parser.add_argument("--long_orfs_scores", dest="long_orfs_scores_filename", type=str, default="", required=True, help="longest_orfs.cds.scores file")
        
    
    args = parser.parse_args()

    long_orfs_cds_file = args.long_orfs_cds_filename
    long_orfs_scored_file = args.long_orfs_scores_filename


    predicted_orf_coords = td.retrieve_orf_coords(long_orfs_cds_file)

    prediction_list = td.parse_predictions_and_scores(long_orfs_scored_file, predicted_orf_coords)

    athal_rpart_tree(prediction_list, predicted_orf_coords)



    sys.exit(0)


def length_normalize(length, frame_scores):
    frame_scores = [ y / 4.0 for y in frame_scores]

    return frame_scores


def athal_rpart_tree(prediction_list, predicted_orf_coords):


    def athal_alg(orf_length, frame_scores):
        frame_scores = length_normalize(orf_length, frame_scores)

        pass_orf = True

        if td.fst_is_max_all(frame_scores):
            if orf_length > 406:
                if frame_scores[0] < -0.0044:
                    pass_orf = False
            else:
                if frame_scores[0] >= 0.0086:
                    if orf_length < 326:
                        pass_orf = False
                else:
                    pass_orf = False
        else:
            if orf_length < 718:
                pass_orf = False

        return pass_orf
    

    athal_orfs = td.select(prediction_list, predicted_orf_coords, athal_alg)

    athal_all_preds_filename = "athal.rpart_all.gff"
    with open(athal_all_preds_filename, 'w') as ofh:
        td.write_preds_to_file(athal_orfs, ofh)

    athal_single_preds_filename = "athal.rpart_single.gff"
    athal_single_orfs = td.select_single_orf_per_transcript(athal_orfs)
    with open(athal_single_preds_filename, 'w') as ofh:
        td.write_preds_to_file(athal_single_orfs, ofh)
    



if __name__ == '__main__':
    main()


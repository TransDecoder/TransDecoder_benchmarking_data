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



    def td_long_orfs(orflen, frame_scores):
        return True

    select(prediction_list, predicted_orf_coords, "td_long_orfs", td_long_orfs)

        
    
    def td_fst_gt_zero(orflen, frame_scores):
        return(td.fst_gt_zero(frame_scores))


    select(prediction_list, predicted_orf_coords, "td_fst_gt_zero", td_fst_gt_zero)


    def td_fst_gt_zero_max_3(orflen, frame_scores):
        return td.fst_gt_zero(frame_scores) and td.fst_is_max3(frame_scores)

    select(prediction_list, predicted_orf_coords, "td_gt0m3", td_fst_gt_zero_max_3)
    
    def td_fst_gt_zero_max_all(orflen, frame_scores):
        return td.fst_gt_zero(frame_scores) and td.fst_is_max_all(frame_scores)

    select(prediction_list, predicted_orf_coords, "td_gt0mAll", td_fst_gt_zero_max_all)



    # supp by length

    def td_fst_gt_zero_max_3_supLength(orflen, frame_scores):
        return orflen >= 700 or (td.fst_gt_zero(frame_scores) and td.fst_is_max3(frame_scores))

    select(prediction_list, predicted_orf_coords, "td_gt0m3Len", td_fst_gt_zero_max_3_supLength)

    def td_fst_gt_zero_max_all_supLength(orflen, frame_scores):
        return orflen >= 700 or (td.fst_gt_zero(frame_scores) and td.fst_is_max_all(frame_scores) )

    select(prediction_list, predicted_orf_coords, "td_gt0mAllLen", td_fst_gt_zero_max_all_supLength)

    
    
    
    sys.exit(0)


def write_outputs(preds, token):
    
    all_preds_filename = token + ".gff"
    sys.stderr.write("writing file: {}\n".format(all_preds_filename))
    with open(all_preds_filename, 'w') as ofh:
        td.write_preds_to_file(preds, ofh)

    single_preds_filename = token + ".single.gff"
    sys.stderr.write("writing file: {}\n".format(single_preds_filename))
    single_orfs = td.select_single_orf_per_transcript(preds)
    with open(single_preds_filename, 'w') as ofh:
        td.write_preds_to_file(single_orfs, ofh)




def select(prediction_list, predicted_orf_coords, token, alg):
    
    orfs = td.select(prediction_list, predicted_orf_coords, alg)

    write_outputs(orfs, token)



if __name__ == '__main__':
    main()


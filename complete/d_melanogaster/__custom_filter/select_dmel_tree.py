#!/usr/bin/env python

import sys, os, re


usage = "\n\n\tusage: {} longest_orfs.cds longest_orfs.cds.scores\n\n"
if len(sys.argv) < 3:
    sys.stderr.write(usage)
    sys.exit(1)

long_orfs_cds_file = sys.argv[1]
long_orfs_scored_file = sys.argv[2]

ORIG_TRANSDECODER_FLAG = False


def main():

    predicted_orf_coords = retrieve_orf_coords(long_orfs_cds_file)

    prediction_list = parse_predictions_and_scores(long_orfs_scored_file, predicted_orf_coords)

    select_dmel(prediction_list, long_orfs_scored_file + ".dmel_tree.gff", predicted_orf_coords)
    
    
    
    sys.exit(0)



def retrieve_orf_coords(long_orfs_cds_file):

    orf_acc_to_coord_info = {}

    with open(long_orfs_cds_file) as fh:
        for line in fh:
            if not re.search("^>", line):
                continue
            match = re.search(" (\S+):(\d+)-(\d+)\(([+-])\)$", line)
            if not match:
                raise RuntimeError("Error, cannot extract orf coord info from line: {}".format(line))
            (transcript_id, lend, rend, orient) = (match.group(1), match.group(2), match.group(3), match.group(4))
            (lend, rend) = sorted((int(lend), int(rend)))

            match = re.search("^>(\S+)", line)
            orf_id = match.group(1)

            orf_acc_to_coord_info[orf_id] = {
                'transcript_id' : transcript_id,
                'lend' : lend,
                'rend' : rend,
                'orient' : orient }


    return orf_acc_to_coord_info


def parse_predictions_and_scores(long_orfs_scored_file, predicted_orf_coords):
        
    prediction_list = []
    
    fh = open(long_orfs_scored_file)

    for line in fh:
        if re.search("^#", line): continue
        line = line.rstrip()
        (orf_id, markov_order, orf_length, score_1, score_2, score_3, score_4, score_5, score_6)  = line.split("\t")

        orf_length = int(orf_length)
        score_1 = float(score_1)
        score_2 = float(score_2)
        score_3 = float(score_3)
        score_4 = float(score_4)
        score_5 = float(score_5)
        score_6 = float(score_6)


        orf_struct = predicted_orf_coords[orf_id]

        prediction = { 'orf_id' : orf_id,
                       'markov_order' : markov_order,
                       'orf_length' : orf_length,
                       'frame_scores' : (score_1, score_2, score_3, score_4, score_5, score_6),
                       'orf_struct' : orf_struct
                       }

        prediction_list.append(prediction)



    prediction_list.sort(key=lambda x: x['orf_length'])

    prediction_list.reverse()

    return prediction_list



def select_dmel(prediction_list, output_file, predicted_orf_coords):

    long_orf_size = 1000
    moderate_orf_size = 500
    
    sys.stderr.write("-writing {}\n".format(output_file))
    
    ofh = open(output_file, 'w')

    seen_orf_ids = set() 
    seen_transcript_ids = set()

    longest_single_orf = True

    import collections
    
    transcript_to_selected_orfs = collections.defaultdict(list)

    for prediction in prediction_list:

        orf_id = prediction['orf_id']
        markov_order = prediction['markov_order']
        orf_length = prediction['orf_length']
        frame_scores = prediction['frame_scores']
        (score_1, score_2, score_3, score_4, score_5, score_6) = frame_scores

        orf_struct = prediction['orf_struct']

        transcript_id = orf_struct['transcript_id']
        lend = orf_struct['lend']
        rend = orf_struct['rend']
        orient = orf_struct['orient']



        ###########################
        ## apply filtering criteria
        pass_orf = True

        fst_is_max = (frame_scores[0] > max(frame_scores[1:]))
        fst_gt_zero = (frame_scores[0] > 0)
        fst_max3 = (frame_scores[0] > max(frame_scores[1:3]))

        if not fst_is_max:
            pass_orf = False
        elif score_1 < -0.0096:
            pass_orf = False
        
        if pass_orf:

            transcript_to_selected_orfs[transcript_id].append(prediction)


    for transcript_id in transcript_to_selected_orfs:

        prediction_list = transcript_to_selected_orfs[transcript_id]

        
        if ORIG_TRANSDECODER_FLAG:
            prediction_list.sort(key=lambda x: x['orf_length'], reverse=True)
        else:
            prediction_list.sort(key=lambda x: x['frame_scores'][0], reverse=True)
        
        selected_preds = []
        
        for prediction in prediction_list:
        
            ## passed filters, report it

                                
            # ensure it doesn't overlap a selected one.
            found_overlap = False
            for pred in selected_preds:
                if prediction['orf_struct']['lend'] < pred['orf_struct']['rend'] and \
                   prediction['orf_struct']['rend'] > pred['orf_struct']['lend']:
                    found_overlap = True
                    break
            
            if not found_overlap:
                selected_preds.append(prediction)
        
        selected_preds.sort(key=lambda x: x['orf_length'], reverse=True)

        top_selected_pred = selected_preds[0]
        orf_struct = top_selected_pred['orf_struct']
        
        ofh.write("\t".join([transcript_id, "selected", "CDS",
                             str(orf_struct['lend']), str(orf_struct['rend']), '.',
                             orf_struct['orient'], str(top_selected_pred['frame_scores'][0]), top_selected_pred['orf_id']]) + "\n")
            
           



    return




if __name__ == '__main__':
    main()

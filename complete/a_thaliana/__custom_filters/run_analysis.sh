#!/bin/bash

set -e


~/GITHUB/TransDecoder/util/misc/select_TD_orfs.py --long_orfs_cds longest_orfs.cds --long_orfs_scores longest_orfs.cds.scores --single_best  > longest_orfs.cds.scores.def_single_custom.gff

~/GITHUB/TransDecoder/util/misc/select_TD_orfs.py --long_orfs_cds longest_orfs.cds --long_orfs_scores longest_orfs.cds.scores > longest_orfs.cds.scores.def_all_custom.gff



~/GITHUB/TransDecoder_benchmarking_data/utilities/run_analysis_pipeline.py  data.json analysis_dir/

~/GITHUB/TransDecoder/util/misc/get_FP_FN_scores.py  longest_orfs.cds.scores longest_orfs.cds analysis_dir/def_custom_single.cds.gff.scored | sort -k12,12gr > custom.FP_FNs.dat


 

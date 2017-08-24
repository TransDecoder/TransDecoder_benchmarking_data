#!/bin/bash

set -ev


## td new
~/GITHUB/TransDecoder/util/misc/select_TD_orfs.py --long_orfs_cds longest_orfs.cds --long_orfs_scores longest_orfs.cds.scores --single_best  > longest_orfs.cds.scores.def_single_custom.gff
~/GITHUB/TransDecoder/util/misc/select_TD_orfs.py --long_orfs_cds longest_orfs.cds --long_orfs_scores longest_orfs.cds.scores > longest_orfs.cds.scores.def_all_custom.gff
~/GITHUB/TransDecoder/util/misc/select_TD_orfs.py --long_orfs_cds longest_orfs.cds --long_orfs_scores longest_orfs.cds.scores --all_good_orfs > longest_orfs.cds.scores.def_all_good_custom.gff


## td original
~/GITHUB/TransDecoder/util/misc/select_TD_orfs.py --long_orfs_cds longest_orfs.cds --long_orfs_scores longest_orfs.cds.scores  --all_good_orfs --td_orig > td_orig.all.gff
~/GITHUB/TransDecoder/util/misc/select_TD_orfs.py --long_orfs_cds longest_orfs.cds --long_orfs_scores longest_orfs.cds.scores  --single_best --td_orig > td_orig.single.gff


~/GITHUB/TransDecoder_benchmarking_data/utilities/run_analysis_pipeline.py  data.json analysis_dir/

~/GITHUB/TransDecoder/util/misc/get_FP_FN_scores.py  longest_orfs.cds.scores longest_orfs.cds analysis_dir/def_custom_single.cds.gff.scored | sort -k12,12gr > custom.FP_FNs.dat

../../__rpart/reforg_TD_rpart_selector.py  --long_orfs_cds longest_orfs.cds --long_orfs_scores longest_orfs.cds.scores

~/GITHUB/TransDecoder_benchmarking_data/utilities/run_analysis_pipeline.py data.rpart.single.json single

~/GITHUB/TransDecoder_benchmarking_data/utilities/run_analysis_pipeline.py data.rpart.all.json all



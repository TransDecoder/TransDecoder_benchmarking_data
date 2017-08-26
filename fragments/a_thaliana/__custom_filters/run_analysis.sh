#!/bin/bash

set -ev



## td alg vary

../../../__rpart/vary_TD_selection_rules.py --long_orfs_cds longest_orfs.cds --long_orfs_scores longest_orfs.cds.scores

../../../utilities/run_analysis_pipeline.py data.TDvary.json analysis_TDvary

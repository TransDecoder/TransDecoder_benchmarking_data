# benchmarking using complete reference orfs

Comparisons include:
*  GeneMarkS-T and -SS (strand-specific mode)
*  Prodigal and -SS 
*  TransDecoder and -SS, -noRS (no refine-start), AGO (all good orfs)
*  LongOrfs and -SS


Benchmarking methods:
*  3prime: only a 3-prime coordinate match is required for TPs.
*  5,3prime:  both a 5-prime and 3-prime coordinate match are required for TPs - else if 3'-only, treated as FN.


## Mouse

Mouse reference sequences

*  [3prime](m_musculus/analysis_dir/accuracy_summary.pdf)
*  [5,3prime](m_musculus/analysis_dir/accuracy_summary.strict.pdf)

Mouse reference sequences + random sequences

*  [3prime](m_musculus/analysis_dir_wRand/accuracy_summary.pdf)
*  [5,3prime](m_musculus/analysis_dir_wRand/accuracy_summary.strict.pdf)


Mouse ref + random, TransDecoder run with varied parameter settings

*  [3prime](m_musculus/analysis_dir_wRand_TDvar/accuracy_summary.pdf)
*  [5,3prime](m_musculus/analysis_dir_wRand_TDvar/accuracy_summary.strict.pdf)

## Drosophila

Drosophila reference sequences

*  [3prime](d_melanogaster/analysis_dir/accuracy_summary.pdf)
*  [5,3prime](d_melanogaster/analysis_dir/accuracy_summary.strict.pdf)

Drosoph + random

*  [3prime](d_melanogaster/analysis_dir_wRand/accuracy_summary.pdf)
*  [5,3prime](d_melanogaster/analysis_dir_wRand/accuracy_summary.strict.pdf)

Drosoph + random, TD varied params

*  [3prime](d_melanogaster/analysis_dir_wRand_TDvar/accuracy_summary.pdf)
*  [5,3prime](d_melanogaster/analysis_dir_wRand_TDvar/accuracy_summary.strict.pdf)


## Arabidopsis


Arabidopsis reference sequences

*  [3prime](a_thaliana/analysis_dir/accuracy_summary.pdf)
*  [5,3prime](a_thaliana/analysis_dir/accuracy_summary.strict.pdf)

Arabidopsis + random

*  [3prime](a_thaliana/analysis_dir_wRand/accuracy_summary.pdf)
*  [5,3prime](a_thaliana/analysis_dir_wRand/accuracy_summary.strict.pdf)

Arabidopsis + random, TD varied params

*  [3prime](a_thaliana/analysis_dir_wRand_TDvar/accuracy_summary.pdf)
*  [5,3prime](a_thaliana/analysis_dir_wRand_TDvar/accuracy_summary.strict.pdf)


## S. pombe

S. pombe reference sequences

*  [3prime](s_pombe/analysis_dir/accuracy_summary.pdf)
*  [5,3prime](s_pombe/analysis_dir/accuracy_summary.strict.pdf)

S. pombe + random

*  [3prime](s_pombe/analysis_dir_wRand/accuracy_summary.pdf)
*  [5,3prime](s_pombe/analysis_dir_wRand/accuracy_summary.strict.pdf)

S. pombe + random, TD varied params

*  [3prime](s_pombe/analysis_dir_wRand_TDvar/accuracy_summary.pdf)
*  [5,3prime](s_pombe/analysis_dir_wRand_TDvar/accuracy_summary.strict.pdf)


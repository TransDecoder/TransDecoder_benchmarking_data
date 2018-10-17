# TransDecoder_benchmarking_data
transdecoder benchmarking data and analysis routines



Ways to rerun transdecoder:

## by grid / parallel:
find . -type d -regex ".*transdecoder_dir.*" -exec rm -rf {} \;
find . |grep pipeliner | grep TransDecoder | xargs -n 1 rm -f 

~/utilities/trinity_uger_cmd_processor.py td.cmds 1  2>&1 | tee td.cmds.log


## serially (slow):

make rerun_TransDecoder PRECLEAN=TRUE




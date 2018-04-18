

analyze:
	../../utilities/run_analysis_pipeline.py data.json  analysis_dir
	../../utilities/run_analysis_pipeline.py data.wRand.json  analysis_dir_wRand
	../../utilities/run_analysis_pipeline.py data.wRand.TDvar.json  analysis_dir_wRand_TDvar



clean:
	rm -rf ./analysis_dir*
	rm -f ./*.pdf

rerun_TransDecoder:
	./rerun_TransDecoder.sh

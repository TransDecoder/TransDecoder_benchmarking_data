#!/bin/bash

set -ev

# rerun 'regular'
rm -rf output_files/TransDecoder/* && \
    cd output_files/TransDecoder  && \
    ../../../../../TransDecoder/TransDecoder.LongOrfs -t ../../input_files/athal.ref_transcripts.fasta.gz && \
    ../../../../../TransDecoder/TransDecoder.Predict -t ../../input_files/athal.ref_transcripts.fasta.gz


# rerun 'regular + strand-specific'
rm -rf output_files/TransDecoder-SS/* && \
    cd output_files/TransDecoder-SS  && \
    ../../../../../TransDecoder/TransDecoder.LongOrfs -S -t ../../input_files/athal.ref_transcripts.fasta.gz && \
    ../../../../../TransDecoder/TransDecoder.Predict -t ../../input_files/athal.ref_transcripts.fasta.gz

# rerun 'wRand'
# rerun 'regular'
rm -rf output_files_wRand/TransDecoder/* && \
    cd output_files_wRand/TransDecoder  && \
    ../../../../../TransDecoder/TransDecoder.LongOrfs -t ../../input_files/athal.ref_transcripts.fasta.wRand.gz && \
    ../../../../../TransDecoder/TransDecoder.Predict -t ../../input_files/athal.ref_transcripts.fasta.wRand.gz


# rerun 'regular + strand-specific'
rm -rf output_files_wRand/TransDecoder-SS/* && \
    cd output_files_wRand/TransDecoder-SS  && \
    ../../../../../TransDecoder/TransDecoder.LongOrfs -S -t ../../input_files/athal.ref_transcripts.fasta.wRand.gz && \
    ../../../../../TransDecoder/TransDecoder.Predict -t ../../input_files/athal.ref_transcripts.fasta.wRand.gz



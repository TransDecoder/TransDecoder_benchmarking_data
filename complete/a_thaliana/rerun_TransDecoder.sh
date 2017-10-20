#!/bin/bash

set -ev

BASEDIR=${PWD}

PRECLEAN=$1

# rerun 'regular'
if [ $PRECLEAN ]; then
    rm -rf output_files/TransDecoder/*
fi

cd output_files/TransDecoder  && \
    ../../../../../TransDecoder/TransDecoder.LongOrfs -t ../../input_files/athal.ref_transcripts.fasta.gz && \
    ../../../../../TransDecoder/TransDecoder.Predict -t ../../input_files/athal.ref_transcripts.fasta.gz


# rerun 'regular + strand-specific'
cd $BASEDIR
if [ $PRECLEAN ]; then
    rm -rf output_files/TransDecoder-SS/*
fi

cd output_files/TransDecoder-SS  && \
    ../../../../../TransDecoder/TransDecoder.LongOrfs -S -t ../../input_files/athal.ref_transcripts.fasta.gz && \
    ../../../../../TransDecoder/TransDecoder.Predict -t ../../input_files/athal.ref_transcripts.fasta.gz

# rerun 'wRand'
cd $BASEDIR
if [ $PRECLEAN ]; then
    rm -rf output_files_wRand/TransDecoder/*
fi

cd output_files_wRand/TransDecoder  && \
    ../../../../../TransDecoder/TransDecoder.LongOrfs -t ../../input_files/athal.ref_transcripts.fasta.wRand.gz && \
    ../../../../../TransDecoder/TransDecoder.Predict -t ../../input_files/athal.ref_transcripts.fasta.wRand.gz


# rerun 'regular + strand-specific'
cd $BASEDIR
if [ $PRECLEAN ]; then
    rm -rf output_files_wRand/TransDecoder-SS/*
fi

cd output_files_wRand/TransDecoder-SS  && \
    ../../../../../TransDecoder/TransDecoder.LongOrfs -S -t ../../input_files/athal.ref_transcripts.fasta.wRand.gz && \
    ../../../../../TransDecoder/TransDecoder.Predict -t ../../input_files/athal.ref_transcripts.fasta.wRand.gz



#!/bin/bash
#PBS -l walltime=72:00:00,mem=9Gb

export PYTHONPATH=/shared/
python /shared/sRNAtoolbox/core/pipelines/runPipelines.py $key $name $outdir $pipeline -c $configure

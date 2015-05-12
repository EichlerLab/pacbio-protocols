#!/bin/bash

export SMRT_ROOT=/net/eichler/vol20/projects/pacbio/opt/smrtanalysis
export SMRT_PATH_PREPEND=/opt/dell/srvadmin/bin:/opt/uge/bin/lx-amd64:/opt/uge/local:/sbin:/usr/bin:/usr/local/bin:/usr/local/sbin:/usr/sbin
export SMRT_ENV_PASSTHROUGH_VARS="SGE_CLUSTER SGE_CELL SGE_LOAD_AVG SGE_ROOT"

. /etc/profile.d/modules.sh
if test ! -z $MODULESHOME; then
   module purge
   module load modules modules-init modules-gs/prod modules-eichler/prod
fi

unset PYTHONPATH
module unload python
module load python/2.7.2
module load perl/5.14.2
module load cross_match/latest
module load bedtools/latest
module unload R
module load R/2.15.0
module load samtools/1.1
export MAKEDIR=/net/eichler/vol4/home/jlhudd/projects/pacbio/smrtanalysis-2.3.0

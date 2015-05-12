#!/bin/bash

if [[ "$#" -ne "4" ]]
then
    echo "Usage: $0 script_dir input.start.fofn vector.align cpus"
    exit 1
fi

MAKEDIR=$1
INPUT=$2
OUTPUT=$3
CPUS=$4
REFERENCE=${MAKEDIR}/vecscreen_and_ecoli.fasta

. ${MAKEDIR}/config.sh
. ${SMRT_ROOT}/current/etc/setup.sh && blasr ${INPUT} ${REFERENCE} -bestn 1 -header -nproc ${CPUS} -out ${OUTPUT}

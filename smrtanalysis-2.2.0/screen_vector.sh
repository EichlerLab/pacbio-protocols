#!/bin/bash

if [[ "$#" -ne "3" ]]
then
    echo "Usage: $0 input.start.fofn vector.align cpus"
    exit 1
fi

. ${MAKEDIR}/config.sh

INPUT=$1
OUTPUT=$2
CPUS=$3

blasr ${INPUT} ${MAKEDIR}/vecscreen_and_ecoli.fasta -bestn 1 -header -nproc ${CPUS} -out ${OUTPUT}

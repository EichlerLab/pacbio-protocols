#!/bin/env python
"""
Create a whitelist for HGAP assembly based on vector screening blacklist.

Based on code from:

https://github.com/PacificBiosciences/Bioinformatics-Training/wiki/HGAP-Whitelisting-Tutorial
"""
import argparse
import csv
import h5py
import os
import re


def get_hole_number_by_file(input_filename):
    """
    Given a path to a .bas.h5 file, return the number of holes in the SMRT cell.
    """
    hdf5_file = h5py.File(input_filename, "r")

    # Assume .bas.h5 file is a multi-part file by default. If the multi-part key
    # doesn't exist, the file is from an earlier iteration of the SMRT cell data
    # format.
    try:
        hole_number = hdf5_file["/MultiPart/HoleLookup"].len()
    except KeyError:
        hole_number = hdf5_file["/PulseData/BaseCalls/ZMW/HoleNumber"].len()

    return hole_number


def get_hole_numbers_by_prefix(inputs_filename):
    """
    Given an input file (input.start.fofn) with paths to .bax.h5 or .bas.h5
    files, determine each unique movie prefix and the total number of holes in
    each movie's SMRT cell.
    """
    with open(inputs_filename, "r") as inputs_fh:
        # Rename .bax.h5 files to .bas.h5 to get hole numbers.
        input_files = list(set([re.sub(r'.[1-3].bax.h5', '.bas.h5', input_file.strip())
                                for input_file in inputs_fh]))

    hole_numbers_by_prefix = {}
    for input_file in input_files:
        movie_prefix = os.path.basename(input_file).replace(".bas.h5", "")
        holes = get_hole_number_by_file(input_file)
        hole_numbers_by_prefix[movie_prefix] = holes

    return hole_numbers_by_prefix


def create_whitelist(blacklist_filename, inputs_filename):
    """
    Prints a list of whitelisted read names by movie prefix and hole numbers for
    a given BLASR alignment and list of input files.
    """
    blacklist_by_prefix = {}
    hole_numbers_by_prefix = get_hole_numbers_by_prefix(inputs_filename)

    with open(blacklist_filename, "r") as blacklist_fh:
        reader = csv.DictReader(blacklist_fh, delimiter=" ")
        for row in reader:
            alignment_id_parts = row["qName"].split("/")
            movie_prefix, hole_number, remainder = row["qName"].split("/", 2)

            blacklist_by_prefix.setdefault(movie_prefix, set()).add(int(hole_number))

    for movie_prefix, blacklist in blacklist_by_prefix.iteritems():
        all_holes = set(range(hole_numbers_by_prefix[movie_prefix]))
        whitelist = all_holes - blacklist
        for hole in whitelist:
            print "/".join((movie_prefix, str(hole)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("blacklist", help="BLASR output (with header) for one or more SMRT cells aligned against vector sequence.")
    parser.add_argument("input_file", help="List of absolute paths to SMRT cell files in an .fofn file.")
    args = parser.parse_args()

    create_whitelist(args.blacklist, args.input_file)

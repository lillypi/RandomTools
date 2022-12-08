#! /usr/bin/env python
"""
Fastq Maker, parsing fasta file
Created on 12/8/2022

The script runs as: 
python fastqMaker.py <fasta> <outdir> -w --force --k 

-w is default = 100 
-f is default = FALSE
-k is default = FALSE

The purpose of this is to parse a fasta file that looks like this: 

>GENE1
ATGTA
>GENE2
ACGT

into a fastq file that will output a shredded fastq file filled with a input # of windows (w) you want. 

Output would then look like this in file1 (named GENE1) if given w = 3: 

@1
ATG
+
III
@2
TGT
+
III
@3
GTA
+
III

file2 (named GENE2)

@1
ACG
+
III
@2
CGT
+
III

"""
#import libaries
import argparse
from pathlib import Path
import random

#set up arguments 'fasta', 'outdir', '--force', and '-k'; the ones with - are optional
ap = argparse.ArgumentParser()
ap.add_argument(
    "fasta", help="FASTA file input; each sequence must be on a single line"
)
ap.add_argument(
    "outdir",
    help="""Output directory; each FASTA record will result in a FASTQ file in
    this directory. Will be created (creating subdirectories as needed), and
    will raise an exception if it already exists""",
)
ap.add_argument(
    "-w", default=100, type=int, help="Size of resulting reads, default is %(default)s"
)
ap.add_argument(
    "-f", "--force", action="store_true", help="Overwrite files in the output directory"
)
ap.add_argument(
    "-k",
    type=int,
    help="""Max number of (randomly-selected) sequences to output. If not
    specified, will output ALL subsequences""",
)
args = ap.parse_args()

#Start Parsing the fasta file 
#Create a dictionary that will hold all of the > lines as keys and the not > lines as values
d = {}
with open(args.fasta) as fin:
    for i, line in enumerate(fin):
        line = line.strip()
        if i % 2 == 0:
            name = line.replace(">", "")
        else:
            d[name] = line

#Setting the args defaults
w = args.w
out = Path(args.outdir)
out.mkdir(parents=True, exist_ok=args.force)

#For every key-value (name-seq) pair in the dictionary, check if it asked for the -k arg
#Create a new fastq file for each of the names and write out the fastq sequence
for name, seq in d.items():
    with open(f"{out}/{name}.fastq", "w") as fout:

        if args.k:
            keepers = random.sample(range(len(seq) - (w - 1)), k=args.k)
        #for every letter (i) in the sequence, minus the sliding window -1 (python starts at 0))
        for i in range(len(seq) - (w - 1)):

            if args.k and i not in keepers:
                continue
            subseq = seq[i : i + w]
            fout.write(f"@{i}\n")
            fout.write(f"{subseq}\n")
            fout.write("+\n")
            fout.write(("I" * w) + "\n")

#!/usr/bin/python3
""" Remove redundant PDBs, i.e. PDBs with the same sequences
    Read line by line, calculate and compare hashes of relevant information.

    Copyright 2019 Fabian Krause
"""

import sys, os, re, hashlib

def calcChecksum(filepath):
    """ Calculate MD5 of relevant information
        Returns tuple of filename and calculated hash
    """
    with open(filepath, "r") as fil:
        cnt = fil.readlines()
        relinfo = []
        for line in cnt:
            atm = line[12:16].rstrip().lstrip()
            altloc = line[16]
            if (atm == "CA"):
                if (altloc == ' '):
                    AA = line[17:20].rstrip().lstrip()
                    relinfo.append(AA)
                else:
                    return None
        return (filepath, hashlib.md5("".join(relinfo).encode("utf-8")).hexdigest())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 duplrem.py infolder outfolder\n"
                "       outfolder contains only non-redundant files")
        sys.exit()

    if len(sys.argv) == 3:
        i = 0
        # cwd = os.curdir
        indir = sys.argv[1]
        outdir = sys.argv[2]
        fils = []
        for (dirpath, dirnames, filenames) in os.walk(indir):
            for fil in filenames:
                chksum = calcChecksum(os.path.join(dirpath, fil))
                if (chksum != None):
                    fils.append(calcChecksum(os.path.join(dirpath, fil)))
        """
        # n^2 approach for testing
        for fil1 in fils:
            for fil2 in fils:
                if fil1[1] == fil2[1] and fil1[0] != fil2[0]:
                    print(fil1)
                    print(fil2)
                    print("----" * 20)
        """
        # Use set (implemented in C therefore performant) to remove duplicates
        nodupl = set([x[1] for x in fils])
        # Keep only one file per calculated hash, move first hit to outfolder
        for fil in fils:
            if fil[1] in nodupl:
                i += 1
                nodupl.remove(fil[1])
                os.rename(fil[0], os.path.join(outdir, os.path.basename(fil[0])))
        print("Found {} duplicate(s)!".format(len(fils) - i))

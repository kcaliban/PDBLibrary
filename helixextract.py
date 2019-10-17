#!/usr/bin/python3
""" Script to slice PDB files into their helices
    Input: File or folder of PDB files
    Output: File or folder of helices extracted from input

    Copyright 2019 iGEM Team Freiburg 2019
"""

import sys, os, re

# Regex for getting Helices lines
REHELIX = re.compile("^HELIX.*$", re.MULTILINE)
# Regex for getting all ATOMS
REATOM = re.compile("^ATOM.*$|^HETATM.*$", re.MULTILINE)

def processPdbFile(filename, outdir):
    """ Returns HelixSlice objects for given PDB file
        Complexity: Let
                        n - number of helices
                        m - number of atoms in PDB file (~ size of file)
                    Time: O((m + 1) * n)
                    More efficient with PQ? Don't have to iterate through all helices
    """
    with open(filename, 'r') as fil:
        content = fil.read()
        # Collect helix lines
        helices = REHELIX.findall(content)
        if len(helices) == 0:
            # No helices in file
            return
        # Collect atoms
        atoms = REATOM.findall(content)
        # Gather helix information
        helixinf = []
        number = 0
        for helix in helices:
            number += 1
            # -- Read helix data from line
            # According to PDB Format specification V33
            # Begin in columns 22-25, insertion code in 26
            # End in columns 34-37, insertion code in 38
            # Columns in document start at 1, python strings indices start at 0
            chainbegin = helix[19]
            begin = int(helix[21:25])
            icodebegin = helix[25]
            chainend = helix[31]
            end = int(helix[33:37])
            icodeend = helix[37]
            # No length specified (a few out of 155k files...) => skip
            if (not helix[71:76].strip()):
                continue
            length = int(helix[71:76])
            helixinf.append([begin, icodebegin, end, icodeend, length, number, chainbegin, chainend])

        # List of currently worked on files and their end data
        # E.g. [FILE, ENDSEQ, ENDINS]
        files = []
        # Iterate through atoms only once by keeping a list of currently worked on helices
        oldseq = None
        oldins = None
        for atom in atoms:
            todelh = []
            todelf = []
            seq = int(atom[22:26])
            ins = atom[26]
            chainid = atom[21]
            for helix in helixinf:
                # Helix starts at current line
                if helix[0] == seq and helix[1] == ins and helix[6] == chainid:
                    outf = open(os.path.join(outdir,str(helix[4]) + "_" + os.path.basename(filename)[:-4] + "_" + str(helix[5]) + ".pdb",
                        ), 'w')
                    files.append([outf, helix[2], helix[3], helix[7]])
                    # Remove helix as it is now in files list
                    todelh.append(helix)
            # Special cases:
            #  * Jump in sequences can happen
            #  * New chain can start
            for ofile in files:
                # If we are past the final sequence, the chain number is different or we are past the end insertion point: close
                if (seq > ofile[1]) or (chainid != ofile[3]) or (seq == ofile[1] and ins > ofile[2]):
                    ofile[0].close()
                    todelf.append(ofile)
                else:
                    # Write current atom
                    ofile[0].write(atom + "\n")
            # Deleting an element from a list while iterating through it: BAD IDEA
            # => separate lists
            for de in todelf:
                files.remove(de)
            for de in todelh:
                helixinf.remove(de)
            todelf = []
            todelh = []
            oldseq = seq
            oldins = ins


if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print("Usage: python3 helixextract.py infolder outfolder"
                "\n       python3 helixextract.py file")
        sys.exit()

    if len(sys.argv) == 3:
        indir = sys.argv[1]
        outdir = sys.argv[2]
        perc = 0
        i = 0
        for (dirpath, dirnames, filenames) in os.walk(indir):
            leng = float(len(filenames))
            for fil in filenames:
                i += 1
                processPdbFile(os.path.join(dirpath, fil), outdir)
                perc = int(i / leng * 100)
                print(str(perc) + "%")
    else:
        infile = sys.argv[1]
        processPdbFile(infile, ".")

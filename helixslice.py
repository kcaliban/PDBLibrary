#!/usr/bin/python3
""" Slices up given PDBs into
    helices of length to be specified
    using a "sliding" window over the helix

    Copyright 2019 Fabian Krause
"""

import sys, os ,re

# Regex for ATOMS
REATOM = re.compile("^ATOM.*$|^HETATM.*$", re.MULTILINE)

def heliSlice(infile, outdir, n):
    """ Using a sliding window, slide over the helix creating new
        helices of length n
    """
    with open(infile, "r") as fil:
        content = fil.read()
        # Collect atoms
        atoms = REATOM.findall(content)
        # Collect their sequence number and insertion point
        atomid = []
        # Count the number of different sequences
        oldid = (0, '')
        seq = 0
        for atom in atoms:
            seqn = int(atom[22:26])
            inp = atom[26]
            newid = (seqn, inp)
            if newid != oldid:
                seq += 1
                oldid = newid
            atomid.append([atom, newid])
        # Not enough sequences
        if seq < n:
            return
        # Create output files
        # Iterating over number of files ~ O(|atoms| * (seq - n))
        # Iterating over atoms and keeping a list ~ O(|atoms| * (seq - n))
        # [FILE, NUMBEROFSEQSOFAR]
        filelist = []
        # Counter to keep track of how many sequences so far
        # (so we can stop @ seq - n)
        noseq = 0
        oldseq = (0, '')
        for atomi in atomid:
            newseq = False
            if atomi[1] != oldseq:
                # print("{} == {}".format(oldseq, atomi[1]))
                noseq += 1
                oldseq = atomi[1]
                newseq = True
            todelf = []
            if newseq and noseq < seq - n + 2:
                filelist.append([open(os.path.join(outdir, os.path.basename(infile)[:-4] + "_" + str(noseq) + ".pdb"), 'w'), 0])
            for ofile in filelist:
                # Update number of sequences
                if newseq:
                    ofile[1] += 1
                # Check if file has n sequences
                if ofile[1] == n + 1:
                    ofile[0].close()
                    todelf.append(ofile)
                else:
                    # Write line and increase counter if new seq
                    # print("{} \t WRITTEN INTO \t {} \t SEQ {}".format(atomi, ofile[0].name, ofile[1]))
                    ofile[0].write(atomi[0] + "\n")
            for de in todelf:
                filelist.remove(de)

if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 3:
        print("Usage: python3 helixslice.py infolder outfolder n"
                "\n       python3 helixslice.py file n")
        sys.exit()

    if len(sys.argv) == 4:
        indir = sys.argv[1]
        outdir = sys.argv[2]
        n = int(sys.argv[3])
        perc = 0
        i = 0
        for (dirpath, dirnames, filenames) in os.walk(indir):
            leng = float(len(filenames))
            for fil in filenames:
                i += 1
                heliSlice(os.path.join(dirpath, fil), outdir, n)
                perc = int(i / leng * 100)
                print(str(perc) + "%")
    else:
        infile = sys.argv[1]
        n = int(sys.argv[2])
        heliSlice(infile, ".", n)

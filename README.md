# PDBLibrary
Toolset to create a library of .pdb files for the virtual screening for possible binders (or for
usage with finDr).

## Dependencies

* python3

## Installation
Simply clone this repository into a directory of your liking
```bash
cd ilikethisdirectory
git clone https://github.com/kcaliban/LtoD.git 
```

## Preparing a library



## Included Tools

### Helix Extractor

Extracts all helices specified in the header of one or more .pdb files.

To extract all helices of length 5 from a single file

```bash
python3 helixextract.py file 5
```

To extract all helices of length 42 from all files in a folder 

```bash
python3 helixextract.py inputdir outputdir 42
```

### Helix Slicer

Slices the helices of .pdb files into parts of specified length
using a "sliding window" of one or more .pdb files.

To slice .pdbs of length 5 from a file

```bash
python3 helixslice.py file 5
```

To slice .pdbs of length 10 from all files in a folder

```bash
python3 helixslice.py inputdir outputdir 10
```

### Duplicate Remover

Removes duplicate sequences in a pool of .pdb files as well as all .pdb files
that contain alternate locations (since these affect AutoDock Vina scores)

Moves one of each duplicate into outputdir

```bash
python3 duplrem.py inputdir outputdir
```

## License
See LICENSE file

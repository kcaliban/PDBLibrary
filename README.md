# PDBLibrary
Toolset to create a library of .pdb files for the virtual screening for possible binders (or for
usage with finDr).

## Dependencies

* python3

## Installation
Simply clone this repository into a directory of your liking
```bash
cd ilikethisdirectory
git clone https://github.com/kcaliban/PDBLibrary.git 
```

## Preparing a library

For this small tutorial we assume that you are in the directory that you have cloned this repository into, if you aren't, `cd ilikethisdirectory`. You need about 200 GB of space for this process, a lot more if you want to not just extract but also slice helices from the Protein Data Bank.


### Getting the latest version of the Protein Data Bank

First, we need to download the latest version of the Protein Data Bank, here into a folder called `PDB`:

```bash
mkdir PDB
cd PDB
wget -r -np -nd ftp://ftp.wwpdb.org/pub/pdb/data/structures/divided/pdb/*
```

This will leave you with a lot of `ent.gz` files.
These are compressed files, so we have to decompress them
(using a for loop since gunzip has a parameter limit).

```bash
for i in *.gz; do gunzip $i; done
```

After this process is done, you need to rename the files.

```bash
for i in *.ent; do rename 's/ent$/pdb/g' $i; done
```

You now have the latest version of the whole Protein Data Bank on your hard drive.
Go back to the original directory by `cd ..`.

### Extracting all helices

To get an even bigger library, you can extract all helices from this dataset using the Helix Extractor.
Make sure you have enough disk space (about 90GB extra) and that you are in the parent directory of `PDB` and execute the following:

```bash
mkdir helices
python3 PDBLibrary/helixextract.py PDB helices
```

This will take a while. After successful completion, the folder `helices`
will contain all helices extracted from the Protein Data Bank. The files 
have the following format:

`HELIXLENGTH_FILENAME_HELIXNUMBER.pdb`

The filenames allow for easier extraction of specified lengths and later identification of
the protein.

If you only want the helices of say length 12, you can copy these into a directory
called e.g. `helices_12` by

```bash
for i in helices/12_*; do cp $i helices_12; done
```

### Removing duplicates and files with alternate locations

A lot of helices, especially short ones, reappear in different proteins.
Also, some structures contain alternate locations for `CA` atoms,
for which both get interpreted as seperate atoms in programs like Autodock Vina.
To make this library ready for tools like Autodock Vina, these files get
discarded.

To remove duplicates and files with alternate locations of helices of length 12:

```
mkdir helices_12_clean
python3 PDBLibrary/duplrem.py helices_12 helices_12_clean
```

The folder `helices_12_clean` now contains only distinct helices and none
with alternate locations.

### Creating even bigger libraries: Slicing helices

To go even further, you can slice helices into smaller helices of specified length(s). This
requires a looot of disk space, so make sure you have enough.

To get helices of length 9 out of our prior extracted helices of length 12:

```bash
mkdir helices_sliced_9
python3 PDBLibrary/helixslice.py helices_12_clean helices_sliced_9
```

To get helices of length 8-12 all prior extracted helices:

```bash
for i in {8..12}; do mkdir helices_sliced_$i; python3 PDBLibrary/helixslice.py helices helices_sliced_$i $i; done
```

## Included Tools

### Helix Extractor

Extracts all helices specified in the header of one or more .pdb files.

To extract all helices from a single file

```bash
python3 helixextract.py file
```

To extract all helices from all files in a folder 

```bash
python3 helixextract.py inputdir outputdir
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

Outputdir contains "cleaned" library. Files only get moved and not copied
for time efficiency.

```bash
python3 duplrem.py inputdir outputdir
```

## License
See LICENSE file

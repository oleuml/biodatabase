# biodatabase
## Python 3 packages
    $ pip install tqdm sqlite3 pandas
## Clone git repository
    $ git clone https://github.com/oleuml/biodatabase.git
## Download resource files
    $ mkdir res
    $ cd res/
    $ wget hgdownload.cse.ucsc.edu/goldenpath/hg38/chromosomes/chr<NUM>.fa.gz
    $ wget ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_27/gencode.v27.annotation.gtf.gz
    $ gunzip *.gz
### Also needed
Also needed `SNPs` from http://genome.ucsc.edu/cgi-bin/hgTables with following configuartion:
- genome: Human
- group: Variation
- track: Common SNPs
- region: genome
- output format: selected fields from primary and related tables
- output file: `chr.snp`

And columns/fields (if you are clicking `"get output"`):
- chrom
- chromStart
- chromEnd
- name
- strand
- refNCBI
- observed
- molType
- class

And store the `output file` in the `resource directory`.
## Run script
    $ python3 run.py -c NUM -a
## You can use the SQLite Browser
### On Arch Linux
    $ yaourt -S sqlitebrowser
### On Mac OS
    $ brew cask install db-browser-for-sqlite

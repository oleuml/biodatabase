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
## Run script
    $ python3 run.py -c NUM -a
## You can use the SQLite Browser
### On Arch Linux
    $ yaourt -S sqlitebrowser
### On Mac OS
    $ brew cask install db-browser-for-sqlite
    


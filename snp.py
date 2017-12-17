import csv
from collections import Sequence
from tqdm import tqdm

class SNP(Sequence):
    def __init__(self, start, stop, name, strand, refNCBI, observed):
        self.start = start
        self.stop = stop
        self.name = name
        self.strand = strand
        self.refNCBI = refNCBI
        self.observed = observed

    def __str__(self):
        return '{},{},{},{},{},{}'.format(self.start, self.stop, self.name, self.strand, self.refNCBI, self.observed)

    def __getitem__(self, key):
        if key == 0:
            return self.start
        if key == 1:
            return self.stop
        if key == 2:
            return self.name
        if key == 3:
            return self.strand
        if key == 4:
            return self.refNCBI
        if key == 5:
            return self.observed
        else:
            raise StopIteration

    def __len__(self):
        return 6

def extract_single_snp(input_file, output_file, chr_n):
    data = []
    with open(input_file, 'r') as f:
        headline = f.readline()

        headline = headline.split()
        i = 0
        CHROM = -1
        START = -1
        STOP = -1
        NAME = -1
        STRAND = -1
        REFNCBI = -1
        OBSERVED = -1
        MOLTYPE = -1
        CLASS = -1

        for item in headline:
            if item == '#chrom':
                CHROM = i
            elif item == 'chromStart':
                START = i
            elif item == 'chromEnd':
                STOP = i
            elif item == 'name':
                NAME = i
            elif item == 'strand':
                STRAND = i
            elif item == 'refNCBI':
                REFNCBI = i
            elif item == 'observed':
                OBSERVED = i
            elif item == 'molType':
                MOLTYPE = i
            elif item == 'class':
                CLASS = i
            i += 1


        for line in tqdm(f):
            line = line.split()
            if line[CHROM] != chr_n or line[STRAND] != '+' or line[MOLTYPE] != 'genomic' or line[CLASS] != 'single':
                continue
            start = int(line[START])
            stop = int(line[STOP])
            if stop - start == 0 or stop - start == 1:
                data.append(SNP(start=int(line[START]),
                                stop=int(line[STOP]),
                                name=line[NAME],
                                strand=line[STRAND],
                                refNCBI=line[REFNCBI],
                                observed=line[OBSERVED]))

    with open(output_file, 'w', newline = '') as csv_f:
        writer = csv.writer(csv_f)
        header = ['start', 'stop', 'name', 'start', 'refNCBI', 'observed']
        writer.writerow(header)
        for snp in data:
            writer.writerow(snp)

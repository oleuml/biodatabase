import csv
from collections import Sequence
from tqdm import tqdm

GENE = 0
EXON = 1
INTRON = 2
PROMOTER = 3
ENHANCER = 4

class Item(Sequence):
    def __init__(self, type, start, stop, level=1): # TODO: Level
        if start > stop:
            raise Exception('Start position must be less than or equal to stop position: {} > {}'.format(start, stop))
        self.type = type
        self.start = start
        self.stop = stop
        self.level = level

    def __str__(self):
        return '{},{},{},{}'.format(self.type, self.start, self.stop, self.level)

    def __lt__(self, other):
        return self.start <= other.start

    def __getitem__(self, key):
        if key == 0:
            return self.type
        if key == 1:
            return self.start
        if key == 2:
            return self.stop
        if key == 3:
            return self.level
        else:
            raise StopIteration

    def __len__(self):
        return 4

class Gene(Sequence):
    def __init__(self, start, stop, level):
        self.gene = Item(type=GENE, start=start, stop=stop, level=level)
        self.start = start
        self.stop = stop
        self.level = level
        self.exons = []
        self.introns = []
        self.promoter = None
        if self.exons != []:
            update()

    def __str__(self):
        out = [self.gene] + self.exons + self.introns + ([] if self.promoter == None else [self.promoter])
        out.sort()
        s = ''
        for row in out:
            if type(row) == Item:
                s += str(row) + '\n'
        return s

    def __getitem__(self, key):
        if key == 0:
            return self.gene
        elif key < len(self.exons) + 1:
            return self.exons[key-1]
        elif key < len(self.introns) + len(self.exons) + 1:
            return self.introns[key-(len(self.exons) + 1)]
        elif key == 1 + len(self.exons) + len(self.introns):
            return self.promoter
        else:
            raise StopIteration 

    def __len__(self):
        return len(self.exons) + len(self.introns) + (0 if self.promoter == None else 1) + 1

    def add_exon(self, exon):
        '''Add exon to gene. After one or multiple exons be added then is an update needed
        Keyword arguments:
        exon -- Item exon
        '''
        if type(exon) != Item:
            raise TypeError('Exon must be type of Item')
        if exon.type != EXON:
            raise TypeError('ExonItem is not type of EXON')
        self.exons.append(exon)

    def update(self):
        '''Needed if new exons be added. Execute the merging of exons and
           the generating of promoter and introns'''
        if self.exons == []:
            raise Exception('No Exons available.')
        self.merge_exons()
        self.generate_promoter()
        self.generate_introns()

    def generate_introns(self):
        # TODO: level: Wenn 1,2900685,2900821,2
        #                   1,2900711,2900821,1
        # als Beispiel funktioniert nicht, da 2900821 als neuer Start genommen wird.
        # dann aber 2900821 größer als das neue Ende 2900711.
        # Diese beiden Exons werden auch nicht gemerged, wenn die Level unterschiedlich sind. 

        introns = []
        exons = self.exons
        start = exons[0].stop
        stop = self.gene.stop
        for exon in exons[1:]:
            stop = exon.start
            if start+1 <= stop-1:
                intron = Item(INTRON, start+1, stop-1, self.level)
                introns.append(intron)
            start = exon.stop
            # TODO: Gene end last intron??
        self.introns = introns

    def generate_promoter(self):
        '''Generate the promoter of the gene and set the promoter.'''
        exon = self.exons[0]
        start = exon.start
        self.promoter = Item(PROMOTER, start-500, start, self.level) #TODO: stop from Promoter

    def merge_exons(self):
        data = []
        for level in [1, 2]:
            data += self.merge_exons_helper(self.exons, level)
        data.sort()

        self.exons = data

    def merge_exons_helper(self, exons, level):
        data = []
        for exon in exons:
            if exon.level == level:
                data.append(exon)
        if data == []:
            return data
        exons = data
        exons.sort()
        data = []
        new_exon = exons[0]
        for exon in exons[1:]:
            start = new_exon.start
            stop = new_exon.stop
            if exon.start > stop:
                data.append(new_exon)
                new_exon = Item(EXON, exon.start, exon.stop, level)
                continue

            if exon.stop > stop:
                new_exon.stop = exon.stop

        data.append(new_exon)
        return data

def extract_genecodes(input_file, output_file, chr_n, header):
    # Create dictionary for saving space.
    lookup = {'gene' : GENE, 'exon' : EXON}

    CHROM = 0
    TYPE = 2
    START = 3
    END = 4

    items = []
    with open(input_file, 'r') as f:
        for line in tqdm(f):
            # Filter whether line begins with chr_n, ignore the rest.
            line = line.split()
            if(line[CHROM] == chr_n):
                
                typ = line[TYPE]
                # Ignoring other types than exon and gene
                if typ != 'exon' and typ != 'gene':
                    continue
                typ = lookup[typ] # type number
                start_pos = line[START] # start position
                end_pos = line[END] # end position

                # Searching level
                for index, i in enumerate(line):
                    next = index + 1
                    if(i == 'level'):
                        level = int(line[next][0])

                # Checking level
                if level != 1 and level != 2:
                    continue

                item = Item(typ, int(start_pos), int(end_pos)) #, level) #TODO LEVELS
                items.append(item)

    genes = []
    i = -1
    for code in items:
        if code.type == GENE:
            genes.append(Gene(code.start, code.stop, code.level))
            i += 1
            continue
        if code.type == EXON:
            genes[i].add_exon(code)

    for gene in genes:
        gene.update()

    # Write genes into csv file.
    with open(output_file, 'w', newline = '') as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow(header)
        for gene in genes:
            for code in gene:
                writer.writerow(code)

import csv

from args import OUT_DIR
from gene import GENE, EXON, INTRON, PROMOTER, ENHANCER

out_id_tables = [
    '{}aminoacidIDs.csv'.format(OUT_DIR),
    '{}modelIDs.csv'.format(OUT_DIR),
    '{}variantIDs.csv'.format(OUT_DIR),
    '{}regionIDs.csv'.format(OUT_DIR)
]

def write_csv_table(output_file, header, table):
    with open(output_file, 'w', newline='') as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow(header)
        for t in table:
            writer.writerow(t)


amino = {'A' : 0, 'C' : 1, 'G' : 2, 'T' : 3}
aminoacids_header = ['id', 'acid']
aminoacids = [
    [amino['A'], 'A'],
    [amino['C'], 'C'],
    [amino['G'], 'G'],
    [amino['T'], 'T']
]

write_csv_table(out_id_tables[0], aminoacids_header, aminoacids)

modelIDs_header = ['id', 'name']
modelIDs = [
    [0, 'CACGTG'],
    [1, 'TGA(C|A)TCA'],
    [2, 'CCAAT|ATTGG']
]

write_csv_table(out_id_tables[1], modelIDs_header, modelIDs)

variantIDs_header = ['id', 'name', 'pos', 'model']
variantIDs = []
# Generates the variations of model CACGTG:
id = 0
for pos, x in enumerate(modelIDs[0][1]):
    for a in ['A', 'C', 'G', 'T']:
        if a == x:
            continue
        variantIDs.append([id, amino[a], pos, modelIDs[0][0]])
        id += 1

write_csv_table(out_id_tables[2], variantIDs_header, variantIDs)

regionIDs_header = ['id', 'region']
regionIDs = [
    [GENE, 'gene'],
    [EXON, 'exon'],
    [INTRON, 'intron'],
    [PROMOTER, 'promoter'],
    [ENHANCER, 'enhancer']
]

write_csv_table(out_id_tables[3], regionIDs_header, regionIDs)

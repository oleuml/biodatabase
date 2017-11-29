###
# Extracts the start and end position for regions on chromosome7.
# (exon, intron, promoter) using regular expressions.
# Requirement:
# annotation file (of genome) in repository
# Output:
# csv file of chromosome 7 as {region, start pos, stop pos, level}
###
import csv
from collections import defaultdict

input_file = 'gencode.v27.annotation.gtf'
result_file = 'chr7_annotations.csv'

# Create dictionary for saving space.
# TODO: CDS, UTR = introns = i; exons = e; stop_codon, gene
lookup = {'transcript' : 't', 'exon' : 'e', 'UTR' : 'i'}
# For labeling all region types that are not relevant.
lookup = defaultdict(lambda: 'n', lookup)

with open(input_file, 'r') as f:
    data = []
    for line in f:
        # Filter whether line begins with chr7, ignore the rest.
        if(line.split()[:1][0] == "chr7"):
            line_splitted = line.split()
            type_of_region = lookup[line_splitted[2:3][0]] # exon, intron, promoter, ...
            start_pos = line_splitted[3:4][0] # start position
            end_pos = line_splitted[4:5][0] # end position
            # As level has no fixed position, but is preceded by 'level':

            # Dirty sln.
            # for i,j in zip(line_splitted, line_splitted[1:]):
            #     if(i == 'level'):
            #         print(j)

            for index, item in enumerate(line_splitted):
                next = index + 1
                if(item == 'level'):
                    level = line_splitted[next][0]
            data_line = [type_of_region, start_pos, end_pos, level]
            data.append(data_line)
            # print("Type: " + str(type_of_region) + " Start: " + str(start_pos) + " End: " + str(end_pos) + " Lvl: " + str(level))

# Write data into csv file.
with open(result_file, 'w', newline = '') as csv_f:
    writer = csv.writer(csv_f)
    for row in data:
        writer.writerow(row)

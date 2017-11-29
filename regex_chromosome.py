###
# Finding all start and end positions of sequences on chromosome
# using regular expressions.
# Requirement:
# chromosome file of chromosome 7 in repository
# Output:
# 1) csv file for each model, respectively, as {start pos, stop pos}
# 2) csv file for each variant, respectively, as {start pos, stop pos}
###
import re
import csv
# Models and variants for first model.
pattern_model1 = r'CACGTG'
pattern_model2 = r'TGA(C|G)TCA'
pattern_model3 = r'CCAAT|ATTGG'
model1_variants = [r'(A|G|T)ACGTG', r'C(C|G|T)CGTG', r'CA(A|G|T)TG', r'CAC(A|C|T)TG', r'CACG(A|C|G)G', r'CACGT(A|C|T)']

# Patterns and corresponding csv files.
# All the files will contain all positions as rows in the format 'start, stop'.
# The variants are calculated for the first model.
all_patterns = [pattern_model1, pattern_model2, pattern_model3]
all_results = ['model1_start_stop.csv', 'model2_start_stop.csv', 'model3_start_stop.csv']
model1_variant_results = ['m1_variant_pos1.csv', 'm1_variant_pos2.csv', 'm1_variant_pos3.csv', 'm1_variant_pos4.csv', 'm1_variant_pos5.csv', 'm1_variant_pos6.csv']

with open('chr7.fa', 'r') as f:
    # Ignore first line (description of sequence).
    data = ''.join(f.read().split('\n')[1:])
    # Store starting and ending pos in csv file.
    for pattern, result in zip(all_patterns, all_results):
        # Find the corresponding pattern (ignoring lower/upper cases).
        it = re.finditer(pattern, data, re.IGNORECASE)
        with open(result, 'w', newline = '') as csv_f:
            writer = csv.writer(csv_f)
            for match_object in it:
                writer.writerow([match_object.start(), match_object.end()])
                # print(match_object)
                # print(match_object.start())
                # print(match_object.end())
    for pattern, result in zip(model1_variants, model1_variant_results):
        # Find the corresponding pattern (ignoring lower/upper cases).
        it = re.finditer(pattern, data, re.IGNORECASE)
        with open(result, 'w', newline = '') as csv_f:
            writer = csv.writer(csv_f)
            for match_object in it:
                writer.writerow([match_object.start(), match_object.end()])

###
# Finding all start and end positions of sequences on chromosome 7
# using regular expressions.
# Requirement:
# chromosome file of chromosome 7 in repository
# Output:
# 1) csv file for all models as {model no, start pos, stop pos}
#    in which model is enumerated
# 2) csv file containing all variants of model 1
#    as {variant pos, start pos, stop pos, model no}
###

import re
import csv
# Models and variants for first model.
pattern_model1 = r'CACGTG'
pattern_model2 = r'TGA(C|G)TCA'
pattern_model3 = r'CCAAT|ATTGG'
model1_variants = [r'(A|G|T)ACGTG', r'C(C|G|T)CGTG', r'CA(A|G|T)TG', r'CAC(A|C|T)TG', r'CACG(A|C|G)G', r'CACGT(A|C|T)']

# Patterns and corresponding csv files.
all_patterns = [pattern_model1, pattern_model2, pattern_model3]
input_file = 'chr7.fa'
result_model = 'model_start_stop.csv'
result_variant = 'variant_start_stop_model.csv'

header_model = ['model', 'start_pos', 'stop_pos']
header_variant = ['variant_pos', 'start_pos', 'stop_pos', 'model']

with open(input_file, 'r') as f:

    # Ignore first line (description of sequence).
    data = ''.join(f.read().split('\n')[1:])
    # Store starting and ending pos (of each model) in csv file.
    with open(result_model, 'w', newline = '') as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow(header_model)
        for count, pattern in enumerate(all_patterns):
            # Find the corresponding pattern (ignoring lower/upper cases).
            it = re.finditer(pattern, data, re.IGNORECASE)
            for match_object in it:
                writer.writerow([count+1, match_object.start(), match_object.end()])

    # Store starting and ending pos(of each variant, for model 1) in csv file.
    with open(result_variant, 'w', newline = '') as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow(header_variant)
        for count, pattern in enumerate(model1_variants):
            # Find the corresponding pattern (ignoring lower/upper cases).
            it = re.finditer(pattern, data, re.IGNORECASE)
            for match_object in it:
                # Hard coding model 1 (as all variants are for model 1).
                # Variants are counted from 0.
                writer.writerow([count, match_object.start(), match_object.end(), 1])

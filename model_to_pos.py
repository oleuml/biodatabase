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
from tqdm import tqdm

def model_to_pos(input_file, output_file, header, patterns):
    with open(input_file, 'r') as f:

        # Ignore first line (description of sequence).
        data = ''.join(f.read().split('\n')[1:])
        # Store starting and ending pos (of each model/pattern) in csv file.
        with open(output_file, 'w', newline = '') as csv_f:
            writer = csv.writer(csv_f)
            writer.writerow(header)
            for count, pattern in enumerate(patterns):
                # Find the corresponding pattern (ignoring lower/upper cases).
                it = re.finditer(pattern, data, re.IGNORECASE)
                for match_object in tqdm(it):
                    # TODO: Warum count + 1???
                    writer.writerow([count+1, match_object.start(), match_object.end()])

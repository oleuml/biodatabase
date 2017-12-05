###
# Create an index of positions for the models and the variants, respectively.
# Requirement:
# 1) files for all models which indicate {start pos, stop pos}
# 2) annotation file as {region, start pos, stop pos, level}
# Output:
# 1) csv file containing (index) pos and corresponding model
# 2) csv file containing (index) pos and corresponding annotations
###

import csv

#TODO: Input files
def creating_indexed_models(input_files, output_file, header):
    # For the Models.
    with open(output_file, 'w', newline = '') as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow(header)
        # Write for each model the corresponding indices.
        for modelnr, model in enumerate(input_files):
            with open(model, 'r') as f:
                for line in f:
                    line_splitted = line.split(',')
                    start = int(line_splitted[0])
                    stop = int(line_splitted[1])
                    # TODO: STOP after string or on last char of string?
                    for index in range(start, stop):
                        # print("x" + str(x) + "modelnr " + str(modelnr))
                        writer.writerow([index, modelnr])

def creating_indexed_annotations(input_file, output_file, header):
    # For the Annotations.
    with open(output_file, 'w', newline = '') as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow(header)
        with open(input_file, 'r') as f:
            for line in f:
                line_splitted = line.split(',')
                region = line_splitted[0]
                start = int(line_splitted[1])
                # TODO: STOP after string or on last char of string?
                stop = int(line_splitted[2])
                level = int(line_splitted[3])
                for index in range(start, stop):
                    writer.writerow([index, region, level])

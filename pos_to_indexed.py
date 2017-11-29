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

all_models = ['model1_start_stop.csv', 'model2_start_stop.csv', 'model3_start_stop.csv']
annotation_file = 'chr7_annotations.csv'

result_file_model = 'pos_to_model.csv'
result_file_region = 'pos_to_region.csv'

header_model = ['pos', 'model']
header_annotation = ['pos', 'region', 'level']

# For the Models.
with open(result_file_model, 'w',newline = '') as csv_f:
    writer = csv.writer(csv_f)
    writer.writerow(header_model)
    # Write for each model the corresponding indices.
    for modelno, model in enumerate(all_models):
        with open(model, 'r') as f:
            for line in f:
                line_splitted = line.split(',')
                start = int(line_splitted[0])
                stop = int(line_splitted[1])
                # TODO: STOP after string or on last char of string?
                for index in range(start,stop):
                    # print("x" + str(x) + "modelno " + str(modelno))
                    writer.writerow([index,modelno])

# For the Annotations.
with open(result_file_region, 'w',newline = '') as csv_f:
    writer = csv.writer(csv_f)
    writer.writerow(header_annotation)
    with open(annotation_file, 'r') as f:
        for line in f:
            line_splitted = line.split(',')
            region = line_splitted[0]
            start = int(line_splitted[1])
            # TODO: STOP after string or on last char of string?
            stop = int(line_splitted[2])
            level = int(line_splitted[3])
            for index in range(start,stop):
                writer.writerow([index, region, level])

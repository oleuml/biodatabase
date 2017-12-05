#!/usr/bin/python3
import os
import sys

# TODO: file names
from args import getOption
from model_to_pos import model_to_pos
from pos_to_indexed import creating_indexed_models, creating_indexed_annotations
from regex_annotation import extract_annotations
from regex_chromosome import finding_patterns
from db import make_sql_database

FINDING = getOption("-finding") or False
CREATING = getOption("-creating") or False
DATABASE = getOption("-database") or False


## RECOURCE & DATA PATH ##
# Path to resources (fasta-files, gtf-files)
res_path = 'res/'
# Path to output/created csv-files
data_path = 'data/'

if not os.path.exists(res_path):
    print("Directory not exists: {}".format(res_path))
    sys.exit(1)
if not os.path.exists(data_path):
    os.makedirs(data_path)

################################################################################
#### FINDING ALL POSITIONS OF PATTERNS ####

## PATTERNS OF MODEL & VARIATIONS ##
# Model and variants for first model.
models = [
    r'CACGTG',
    r'TGA(C|G)TCA',
    r'CCAAT|ATTGG']
model1_variants = [
    r'(A|G|T)ACGTG',
    r'C(C|G|T)CGTG',
    r'CA(A|G|T)TG',
    r'CAC(A|C|T)TG',
    r'CACG(A|C|G)G',
    r'CACGT(A|C|T)']

## CHROMOSOM NAME & FILE PATH ##
# Chromosom name
chr_name = 'chr3'
# Chromosom file path
chr_file = '{}chr3.fa'.format(res_path)

## OUTPUT FILES ##
result_model = '{}model_start_stop.csv'.format(data_path)
result_variant = '{}variant_start_stop_model.csv'.format(data_path)

## HEADERS ##
header_model = ['model', 'start_pos', 'stop_pos']
header_variant = ['variant_pos', 'start_pos', 'stop_pos', 'model']

## ANNOTATIONS FILE PATHS (INPUT/OUTPUT) ##
annotation_input_file = '{}gencode.v27.annotation.gtf'.format(res_path)
annotation_output_file = '{}{}_annotations.csv'.format(data_path, chr_name)

## CHECKS EXISTS ##
if not os.path.exists(chr_file):
    print("File not exists: {}".format(chr_file))
    sys.exit(1)

if not os.path.exists(chr_file):
    print("File not exists: {}".format(annotation_input_file))
    sys.exit(1)

## EXECUTION ##
if FINDING:
    print("Finding all positions of patterns (models & variants) from \"{}\".".format(chr_file))
    model_to_pos(
        input_file=chr_file,
        output_file=result_model,
        header=header_model,
        patterns=models)
    print("Finished extracting positions of model from \"{}\".".format(chr_file))
    model_to_pos(
        input_file=chr_file,
        output_file=result_variant,
        header=header_variant,
        patterns=model1_variants)
    print("Finished extracting positions of variants from \"{}\".".format(chr_file))

    print("Extracting annotations from \"{}\".".format(annotation_input_file))
    extract_annotations(
        input_file=annotation_input_file,
        output_file=annotation_output_file,
        chr_n=chr_name)
    print("Finished extracting annotations from \"{}\".".format(annotation_input_file))

################################################################################
#### CREATING ALL INDICES WITH CORRESPONDING ANNOTATIONS & MODELS ####

## INPUT FILES ##
all_models = [
    '{}model1_start_stop.csv'.format(data_path),
    '{}model2_start_stop.csv'.format(data_path),
    '{}model3_start_stop.csv'.format(data_path)]
annotation_file = '{}{}_annotations.csv'.format(data_path, chr_name)

## OUTPUT FILES ##
result_file_model = '{}pos_to_model.csv'.format(data_path)
result_file_region = '{}pos_to_region.csv'.format(data_path)

## HEADERS ##
header_model = ['pos', 'model']
header_annotation = ['pos', 'region', 'level']

## EXECUTION ##
if CREATING:
    print("Creating all indices with corresponding models.")
    #TODO: FINDING PATTERNS multiple files???
    finding_patterns(
        input_file=chr_file,
        output_path=data_path)
    #TODO: Input files
    creating_indexed_models(
        input_files=all_models,
        output_file=result_file_model,
        header=header_model)
    print("Finished creating all indices with corresponding models.")
    print("Creating all indices with corresponding annotations.")
    creating_indexed_annotations(
        input_file=annotation_file,
        output_file=result_file_region,
        header=header_annotation)
    print("Finished creating all indices with corresponding annotations.")

################################################################################
#### CREATING DATABASE TABLES ####

if DATABASE:
    database = '{}.db'.format(chr_name)
    database_tables = [
        result_file_model,
        #result_file_region, # TODO: overlarge file
        result_model,
        result_variant,
        annotation_output_file]
    print('Creating \"{}\".'.format(database))
    make_sql_database(
        db_name=database,
        csv_files=database_tables)
    print("Finished creating database tables.")


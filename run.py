#!/usr/bin/python3
import os
import sys

# TODO: file names
from args import *
from model_to_pos import model_to_pos
from pos_to_indexed import creating_indexed_models, creating_indexed_annotations
from gene import find_genecodes
from snp import extract_single_snp
from regex_chromosome import finding_patterns
from db import make_sql_database

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

## OUTPUT FILES ##
result_model = '{}model_start_stop.csv'.format(OUT_DIR)
result_variant = '{}variant_start_stop_model.csv'.format(OUT_DIR)

## HEADERS ##
header_model = ['model', 'start_pos', 'stop_pos']
header_variant = ['variant_pos', 'start_pos', 'stop_pos', 'model']
header_annotation = ['type', 'start', 'stop', 'level']
## ANNOTATIONS FILE PATHS OUTPUT ##
annotation_output_file = '{}{}_annotations.csv'.format(OUT_DIR, CHR_NAME)
snp_output_file = '{}{}_snp.csv'.format(OUT_DIR, CHR_NAME)

## EXECUTION ##
if FINDING:
    print("Finding all positions of patterns (models & variants) from \"{}\".".format(CHR_FILE))
    model_to_pos(
        input_file=CHR_FILE,
        output_file=result_model,
        header=header_model,
        patterns=models)
    print("Finished extracting positions of model from \"{}\".".format(CHR_FILE))
    model_to_pos(
        input_file=CHR_FILE,
        output_file=result_variant,
        header=header_variant,
        patterns=model1_variants)
    print("Finished extracting positions of variants from \"{}\".".format(CHR_FILE))
    
    print("Extracting annotations from \"{}\".".format(ANN_FILE))
    find_genecodes(
        input_file=ANN_FILE,
        output_file=annotation_output_file,
        chr_n=CHR_NAME,
        header=header_annotation)
    print("Finished extracting annotations from \"{}\".".format(ANN_FILE))

    print("Extracting snp from \"{}\"".format(SNP_FILE))
    extract_single_snp(
        input_file=SNP_FILE,
        output_file=snp_output_file,
        chr_n=CHR_NAME)
    print("Finished extracting snp from \"{}\"".format(SNP_FILE))

################################################################################
#### CREATING ALL INDICES WITH CORRESPONDING ANNOTATIONS & MODELS ####

## INPUT FILES ##
all_models = [
    '{}model1_start_stop.csv'.format(OUT_DIR),
    '{}model2_start_stop.csv'.format(OUT_DIR),
    '{}model3_start_stop.csv'.format(OUT_DIR)]
annotation_file = '{}{}_annotations.csv'.format(OUT_DIR, CHR_NAME)

## OUTPUT FILES ##
result_file_model = '{}pos_to_model.csv'.format(OUT_DIR)
result_file_region = '{}pos_to_region.csv'.format(OUT_DIR)

## HEADERS ##
header_model = ['pos', 'model']
header_annotation = ['pos', 'region', 'level']

## EXECUTION ##
if CREATING:
    print("Creating all indices with corresponding models.")
    #TODO: FINDING PATTERNS multiple files???
    finding_patterns(
        input_file=CHR_FILE,
        output_path=OUT_DIR)
    #TODO: Input files
    creating_indexed_models(
        input_files=all_models,
        output_file=result_file_model,
        header=header_model)
    print("Finished creating all indices with corresponding models.")
    # TODO: Could be deleted?
    #print("Creating all indices with corresponding annotations.")
    #creating_indexed_annotations(
    #    input_file=annotation_file,
    #    output_file=result_file_region,
    #    header=header_annotation)
    #print("Finished creating all indices with corresponding annotations.")

################################################################################
#### CREATING DATABASE TABLES ####

if DATABASE:
    database = '{}.db'.format(CHR_NAME)
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


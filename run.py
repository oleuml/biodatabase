#!/usr/bin/python3
import os
import sys

from args import *
from chromosom import extract_patterns
from database import make_sql_database
from gene import extract_genecodes
from snp import extract_single_snp

################################################################################
#### EXTRACTING ALL POSITIONS OF PATTERNS, ALL GENECODES and ALL SNPs ####

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
out_model = '{}{}_models.csv'.format(OUT_DIR, CHR_NAME)
out_variant = '{}{}_variants.csv'.format(OUT_DIR, CHR_NAME)
out_annotation = '{}{}_annotations.csv'.format(OUT_DIR, CHR_NAME)
out_snp = '{}{}_snp.csv'.format(OUT_DIR, CHR_NAME)

## HEADERS ##
header_model = ['model', 'start', 'stop']
header_variant = ['variant', 'start', 'stop', 'model']
header_annotation = ['type', 'start', 'stop', 'level']

## EXECUTION ##
if EXTRACTING:
    print("Extracting all positions of patterns (models & variants) from \"{}\".".format(CHR_FILE))
    extract_patterns(
        input_file=CHR_FILE,
        output_file=out_model,
        header=header_model,
        patterns=models)
    print("Finished extracting positions of model from \"{}\".".format(CHR_FILE))
    extract_patterns(
        input_file=CHR_FILE,
        output_file=out_variant,
        header=header_variant,
        patterns=model1_variants)
    print("Finished extracting positions of variants from \"{}\".".format(CHR_FILE))
    
    print("Extracting annotations from \"{}\".".format(ANN_FILE))
    extract_genecodes(
        input_file=ANN_FILE,
        output_file=out_annotation,
        chr_n=CHR_NAME,
        header=header_annotation)
    print("Finished extracting annotations from \"{}\".".format(ANN_FILE))

    print("Extracting snp from \"{}\"".format(SNP_FILE))
    extract_single_snp(
        input_file=SNP_FILE,
        output_file=out_snp,
        chr_n=CHR_NAME)
    print("Finished extracting snp from \"{}\"".format(SNP_FILE))

################################################################################
#### CREATING DATABASE TABLES ####

if DATABASE:
    database = '{}.db'.format(CHR_NAME)
    database_tables = [
        out_model,
        out_variant,
        out_annotation,
        out_snp]
    print('Creating \"{}\".'.format(database))
    make_sql_database(
        db_name=database,
        csv_files=database_tables)
    print("Finished creating database tables.")


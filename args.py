import argparse
import sys
import os

CHR_NUM = 0
CHR_NAME = 'chr'

OUT_DIR = None
RES_DIR = None
CHR_FILE = None
SNP_FILE = None
ANN_FILE = None

FINDING = False
CREATING = False
DATABASE = False

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--chrnum', nargs=1, metavar='NUM', type=int, choices=range(1,23), help='set number (1-22) of the chromosom', required=True)
parser.add_argument('-a', '--all', help='run all: --finding, --creating, --database', action='store_true')
parser.add_argument('--finding', help='find all positions of patterns', action='store_true')
parser.add_argument('--creating', help='create all indices with corresponding annotations and models', action='store_true')
parser.add_argument('--database', help='create the database tables', action='store_true')

parser.add_argument('--resource-dir', nargs=1, metavar='PATH',help='set the folder of all resource files: chr<NUM>.fa gencode.v<VERSION>.annotation.gtf')
parser.add_argument('--chr-file', nargs=1, metavar='FILE', help='set the file path of the chromosom fasta-file. Isn\'t needed if the file in the resource folder.')
parser.add_argument('--annotation-file', nargs=1, metavar='FILE', help='set the file path of the annotation gtf-file. Isn\'t needed if the file in the resource folder.')
parser.add_argument('--snp-file', nargs=1, metavar='FILE', help='set the file path of the snp file. Isn\'t needed if the file in the resource folder.')
parser.add_argument('--output-dir', nargs=1, metavar='PATH', help='set the folder of all generated files')

args = parser.parse_args()

def error(err, num=1):
    print("Error: {}".format(err))
    sys.exit(num)

def check_exist(path):
    if not os.path.exists(path):
        error("File/Folder not exists {}".format(path))


CHR_NUM = args.chrnum[0]
CHR_NAME = '{}{}'.format(CHR_NAME, CHR_NUM)

#### RESOURCE FILES ####
if args.resource_dir != None:
    RES_DIR = args.resource_dir[0]
    if not RES_DIR.endswith('/'):
        RES_DIR += '/'
else:
    RES_DIR = 'res/'
check_exist(RES_DIR)

if args.chr_file != None:
    CHR_FILE = args.chr_file[0]
else:
    CHR_FILE = '{}{}.fa'.format(RES_DIR, CHR_NAME)
check_exist(CHR_FILE)

if args.annotation_file != None:
    ANN_FILE = args.annotation_file[0]
else:
    for file in os.listdir(RES_DIR):
        if file.startswith('gencode.') and file.endswith('.annotation.gtf'):
            ANN_FILE = '{}{}'.format(RES_DIR, file)
check_exist(ANN_FILE)

if args.snp_file != None:
    SNP_FILE = args.snp_file[0]
else:
    for file in os.listdir(RES_DIR):
        if file.endswith(''): # TODO: add SNP file end
            SNP_FILE = '{}{}'.format(RES_DIR, file)
check_exist(SNP_FILE)

#### OUTPUT FOLDER ####
if args.output_dir != None:
    OUT_DIR = args.output_dir[0]
    if not OUT_DIR.endswith('/'):
        OUT_DIR += '/'

else:
    OUT_DIR = 'out/'
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)


if args.finding:
    FINDING = True
if args.creating:
    CREATING = True
if args.database:
    DATABASE = True
if args.all:
    FINDING = True
    CREATING = True
    DATABASE = True

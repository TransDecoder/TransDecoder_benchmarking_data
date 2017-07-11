#Plot ROC curve from algorithm outputs
from dependency import *
path = os.getcwd()

#add options to inputs
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='Analyse output files\n'+"Usage: python run.py [fasta file] [algorithm] [i = 1,2,3]\n")
parser.add_argument("filename", help= "Input fasta file")
parser.add_argument("algorithm", help="transdecoder, genemark, prodigal")
parser.add_argument('i', metavar='i', type=int,choices = [1,2,3], 
help = '1 - transdecoder.gff3\n'+ '2 - transdecoder_dir/longest_orfs.gff3\n'+ '3 - transdecoder.gff3-single-best\n')
args = parser.parse_args()


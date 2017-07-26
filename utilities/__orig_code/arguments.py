#Store arguments provided by the user and pass them to other scripts in the package
from dependency import *
path = os.getcwd()

#add options to inputs
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='Analyse output files\n'+"Usage: python run.py [fasta file] [algorithm] [i = 1,2,3,4] [strand] [window]\n")
parser.add_argument("filename", help= "Input fasta file")
parser.add_argument("algorithm", help="transdecoder, genemark, prodigal")
parser.add_argument('i', metavar='i', type=int,choices = [1,2,3,4], 
help = '1 - transdecoder.gff3\n'+ '2 - transdecoder_dir/longest_orfs.gff3\n'+ '3 - transdecoder.gff3-single-best\n'+'4 - transdecoder.gff3-refine-starts\n'+'Use any option for Prodigal and GeneMarkS-T\n')
parser.add_argument("strand", help="direct, all\n")
parser.add_argument("window", help="yes, no\n"+'Use window of 2 base shift for fragmented transcripts')
args = parser.parse_args()


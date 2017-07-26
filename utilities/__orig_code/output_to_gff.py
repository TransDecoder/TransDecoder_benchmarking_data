#Create gff file of CDS predictions from Transdecoder, GeneMarkS-T, Prodigal
from dependency import *
from arguments import args
path = os.getcwd()

#convert algorithm outputs to gff format
algo = args.algorithm.lower()
if '/' in args.filename:
    f = args.filename.rsplit('/',1)
    path = path+f[0]
    file_name = f[1]
else:
    file_name = args.filename    
num = args.i

def op2gff():
    if algo == 'transdecoder':
        if num == 1:
            f_pred = open(path+'/'+file_name+'.transdecoder.gff3',"r")
        elif num == 2:
            f_pred = open(path+'/'+file_name+'.transdecoder_dir/longest_orfs.gff3',"r")
        elif num == 3:
            f_pred = open(path+'/'+file_name+'.transdecoder.gff3-single-best',"r")
        elif num == 4:
            f_pred = open(path+'/'+file_name+'.transdecoder.gff3-refine-starts',"r")            
        f_out = open(path+'/'+file_name+'_transdecoder_output.gff',"w")
    elif algo == 'genemark':
        f_pred = open(path+'/'+file_name+'.gff',"r")
        f_out = open(path+'/'+file_name+'_genemark_output.gff',"w")
    elif algo == 'prodigal':
        f_pred = open(path+'/prodigal-'+file_name+'.gff',"r")
        f_out = open(path+'/'+file_name+'_prodigal_output.gff',"w")
    prediction = f_pred.readlines()
    #write CDS prediction to an output file
    for pred in prediction:
        if '\tCDS\t' in pred:
            f_out.write(pred)
    f_pred.close()
    f_out.close()


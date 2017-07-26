#Compares the output of an algorithm with the reference
from dependency import *
from arguments import args
path = os.getcwd()

#arguments
algo = args.algorithm.lower()
if '/' in args.filename:
    f = args.filename.rsplit('/',1)
    path = path+f[0]
    file_name = f[1]
else:
    file_name = args.filename    
strand = args.strand.lower()
window = args.window.lower()

#input files
if '-sense' in file_name:
    f = file_name.replace('-sense','')
else:
    f = file_name

f_all = open(path+"/"+f,"r")
f_pred = open(path+"/"+file_name+"_"+algo+"_output.gff","r")
lines = f_all.readlines()
pred = f_pred.readlines()

#output files
f_out = open(path+"/"+file_name+"_"+algo+"_results","w")

sense_prediction = []
for line in pred:
    if '\t+\t' in line:
        sense_prediction.append(line)

if strand == 'all':
    prediction = pred
elif strand == 'direct':
    prediction = sense_prediction

three_match = []
three_five_match = []
false_pos = []
false_neg = []

#store all annotations
all_ann = []
all_annotation = {}
for line in lines:
    if line.startswith('>'):
          annotation = line.strip().split("|")[0][1:]
          all_ann.append(annotation)
          all_annotation[annotation] = line.strip()

#store all predictions
all_pred_ann = []
for pred in prediction:
     line = pred.strip().split('\t')
     transcript_id = line[0].split('|')[0]
     length = re.findall(r'length\:(.*)\|',line[0])[0]
     ref = re.findall(r'CDS\:(.*)\|length:',line[0])[0]
     ref_st = ref.split('-')[0]
     ref_end = ref.split('-')[1]
     pred_st = line[3]
     pred_end = line[4]
     pred_len = str(int(pred_end)-int(pred_st)+1)
     result = '\t'+transcript_id+'\t'+ref_st+'\t'+ref_end+'\t'+pred_st+'\t'+pred_end+'\t'+length+'\t'+pred_len+'\t'
     if ref_end == pred_end and ref_st == pred_st:
          three_five_match.append('TP'+result+'3,5-prime\n')
     elif abs(int(ref_end) - int(pred_end)) in [0,1,2] and window == 'yes':
             three_match.append('TP'+result+'3-prime\n')
     elif ref_end == pred_end and window == 'no':
          three_match.append('TP'+result+'3-prime\n')
     else:
          false_pos.append('FP'+result+'.\n')
     if not transcript_id in all_pred_ann:
         all_pred_ann.append(transcript_id)

#store missing predictions
no_res = list(set(all_ann)-set(all_pred_ann))
for pred in no_res:
     transcript_id = pred
     res = all_annotation[pred]
     ref = re.findall(r'CDS\:(.*)\|length:',res)[0]
     ref_st = ref.split('-')[0] 
     ref_end = ref.split('-')[1]
     pred_st = '.'
     pred_end = '.'
     pred_len = '.'
     length = re.findall(r'length\:(.*)\|',res)[0]
     result = '\t'+transcript_id+'\t'+ref_st+'\t'+ref_end+'\t'+pred_st+'\t'+pred_end+'\t'+length+'\t'+pred_len+'\t'
     false_neg.append('FN'+result+'.\n')

f_out.write('Status\tTranscript_Id\tRef_St\tRef_End\tPred_St\tPred_End\tTrans_Len\tPred_Len\tMatch'+'\n')

#write to file
def write(lst,file_handle):
    for item in lst:
        f_out.write(item)        

write(three_five_match,f_out)
write(three_match,f_out)
write(false_pos,f_out)
write(false_neg,f_out)

f_all.close()
f_pred.close()
f_out.close()

print len(three_five_match)

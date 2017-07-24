#Compares the output of an algorithm with the reference
from dependency import *
from arguments import args
path = os.getcwd()

#arguments
algo = args.algorithm.lower()
file_name = args.filename

#input files
f_all = open(path+"/"+file_name,"r")
f_pred = open(path+"/"+file_name+"_"+algo+"_output.gff","r")

#output files
f_out = open(path+"/"+file_name+"_"+algo+"_results","w")

lines = f_all.readlines()
prediction = f_pred.readlines()

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
     #length = str(int(pred_end)-int(pred_st)+1)
     result = '\t'+transcript_id+'\t'+ref_st+'\t'+ref_end+'\t'+pred_st+'\t'+pred_end+'\t'+length+'\t'
     if ref_end == pred_end and ref_st == pred_st:
          three_five_match.append('TP'+result+'3,5-prime\n')
     elif ref_end == pred_end:
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
     length = re.findall(r'length\:(.*)\|',res)[0]
     result = '\t'+transcript_id+'\t'+ref_st+'\t'+ref_end+'\t'+pred_st+'\t'+pred_end+'\t'+length+'\t'
     false_neg.append('FN'+result+'.\n')

f_out.write('Status\tTranscript_Id\tRef_St\tRef_End\tPred_St\tPred_End\tLength\tMatch'+'\n')

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

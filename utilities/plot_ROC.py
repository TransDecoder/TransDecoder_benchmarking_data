#plot ROC curve of an algorithm
from dependency import *
from arguments import args
path = os.getcwd()

#arguments
algo = args.algorithm.lower()
file_name = args.filename
num = args.i

#input files
f_pred = open(path+"/"+file_name+"_"+algo+"_results","r")
f_out = open(path+'/'+file_name+'_'+algo+'_statistics',"w")
#output files
prediction = f_pred.readlines()

len_stat = []
for i in range(1,len(prediction)):
     pred = prediction[i]
     pred = pred.split('\t')
     if not pred[0] == 'FN': 
         l = [int(pred[5])-int(pred[4]),pred[0]]
         len_stat.append(l)
sort_len_stat = sorted(len_stat)
total = len(prediction)

#calculate sensitivity and specificity for a given list
def extract_range(lst,tp,fp,fn,th_st,th_end):
      for l in lst:
                    if l[1] == "TP":
                         tp +=1              
                    if l[1] ==  "FP":
                         fp +=1
      fn = total-tp
      sensitivity = float(tp)/float(tp+fn)
      specificity = float(tp)/float(tp+fp)
      f_out.write(tp,'\t',fp,'\t',fn,'\t',sensitivity,'\t',1-specificity,'\t',th_st,'\t',th_end)    
      return sensitivity, 1-specificity

f_out.write("TP\tFP\tFN\tSensitivity\tSpecificity\tTheshold_Start\tThreshold_End")

#iterate through the length list with a minimum gene length criteria ranging between 90bp and 480bp with a step of 30bp
x = []
y = []
lst1 = [item[0] for item in sort_len_stat]
lst2 = [item[1] for item in sort_len_stat]
for i in range(90,481,30):
     lst = [ (j,k) for (j,k) in zip(lst1,lst2) if j >= i ]
     a,b = extract_range(lst,0,0,0,lst[0][0],lst[-1][0])
     x.append(a)
     y.append(b)

y_n = y
x_n = x
zero = [0]
one =[1]

#Add zero and one to the end of x and y axis for AUC analysis
y = one+y+zero
x = one+x+zero

# This is the ROC curve
plt.plot(y_n,x_n,marker ='+')

# This is the AUC using built-in function
roc_auc = auc(y, x,reorder = True)

#Calculate using trapezoidal method
auc = 0
for i in range(len(y)-1):
    auc += (y[i+1]-y[i]) * (x[i+1]+x[i])
auc *= 0.5
plt.title(algo.capitalize()+', AUC = %.4f'%roc_auc)
plt.show()

f_pred.close()
f_out.close()

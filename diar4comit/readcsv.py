import csv
import numpy as np

def getcsvfeat(filename):
    

    csv_in = open(filename, 'rb')
    myreader = csv.reader(csv_in)

    k=0
    feature=[]
    temp=[]
    for row in myreader:

          temp=row
          temp1=[]
          for k in range(0,len(temp)):
              temp1.append(float(temp[k]))

          feature.append(temp1) 
    feature=np.array(feature)      
    csv_in.close()
    feature=feature.transpose()
    return feature

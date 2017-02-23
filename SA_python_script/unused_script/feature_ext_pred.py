import csv
import numpy as np
import time
import sys
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score

from sklearn import linear_model

from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

scaler = StandardScaler()
name_file = str(sys.argv[1])

name_new_file = time.strftime( name_file[0:name_file.find(".csv")] +"_predicted_result_%Y-%m-%d_%H-%M-%S")+".csv"

print(name_new_file)


X = []
Y = []
Y_pred = []
target_names = ['sleep','wake']

with open(name_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')    
    #print(readCSV[0]
    feature = np.array(list(readCSV))
    X = feature[1:,:5].astype("float")
    Y = feature[1:,5:]
    print(X[0,:])
    
    scaler.fit(X)
    X = scaler.transform(X)
    print(X[0,:])
    
    
csvfile.close()

#print(Y)

model_name = 'model/MLP_model100k2.sav'
mlp_model = pickle.load(open(model_name,'rb'))
Y_pred = mlp_model.predict(X)
result = mlp_model.score(X,Y);
print(result)

print(classification_report(Y,Y_pred,target_names=target_names))


'''
with open(name_new_file, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(Y_pred)
csvwrite.close()
'''


Y_plot = []
Y_pred_plot = []
for text in Y:
        if text == 'sleep':
            Y_plot.append(1.0)
        else :
            Y_plot.append(0.0)
for text in Y_pred:
        if text == 'sleep':
            Y_pred_plot.append(1.0)
        else :
            Y_pred_plot.append(0.0)

width = 1/1.5
plt.subplot(211)
plt.bar(range(len(Y_plot)),Y_plot,width,color='red',edgecolor='red')
plt.ylabel('state Y',color='r')
plt.subplot(212)
plt.bar(range(len(Y_pred_plot)),Y_pred_plot,width,color = 'blue')

plt.ylabel('state Y pred')
plt.show()

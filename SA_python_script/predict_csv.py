import csv
import numpy as np
import time
import sys
import pickle
import os
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

print "\n============================================"
print "Sleep prediction script started"
print "============================================"

t_start = time.time()
true_start = t_start

scaler = StandardScaler()
name_file = str(sys.argv[1])

X = []
Y = []
Y_pred = []
target_names = ['sleep','wake']

with open(name_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')    
    #print(readCSV[0]
    feature = np.array(list(readCSV))
    X = feature[1:,:5].astype("float")
    
    #print(X[0,:])
    
    scaler.fit(X)
    X = scaler.transform(X)
    #print(X[0,:])
    
    
csvfile.close()
end = time.time() - t_start

print "feature read and normalized time: ", end

t_start = time.time()
#print(Y)

model_name = 'model/MLP_model100k2.sav'
mlp_model = pickle.load(open(model_name,'rb'))
Y_pred = mlp_model.predict(X)
write_file = []
write_file.append('sleep_predicted')
Y_pred_plot = []
for text in Y_pred:
        if text == 'sleep':
            write_file.append(str(0))
        else :
            write_file.append(str(1))

#write_file.append(Y_pred_plot)
end = time.time() - t_start

print "Predicted process time: ", end

t_start = time.time()

name_new_file = time.strftime("predicted/%Y-%m-%d/predicted_result_%H-%M-%S")+".csv"

if not os.path.exists(os.path.dirname(name_new_file)):
    try:
        os.makedirs(os.path.dirname(name_new_file))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
with open(name_new_file, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(write_file)
csvwrite.close()

print "predicted file written dir: "
print os.getcwd() + "/" +name_new_file

end = time.time() - t_start
print "File written time: ", end
true_end = time.time() - true_start
print "Total time: ", true_end
print ""
#result = mlp_model.score(X,Y);
#print(result)

#print(classification_report(Y,Y_pred,target_names=target_names))



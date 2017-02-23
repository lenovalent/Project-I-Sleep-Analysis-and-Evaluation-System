import csv
import numpy as np
import time
import sys
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import validation_curve

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt




scaler = StandardScaler()
name_file = str(sys.argv[1])
name_new_file = time.strftime("hchs-sol-sueno-00306064_%H-%M-%S")+".csv"

# variable for ML
X = []
Y = []
Y_pred = []
target_names = ['sleep','wake']

# get all feature and supervise target from csv file
with open(name_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')    
    feature = np.array(list(readCSV))
    X = feature[1:,:5].astype("float")
    Y = feature[1:,5:]
    scaler.fit(X)
    X = scaler.transform(X)
csvfile.close()

#split data into train set and test set
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

#cross validation method 
cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)

#choose estimator (MLP)
clf = MLPClassifier(solver='lbfgs',learning_rate = 'adaptive', alpha=1e-5,hidden_layer_sizes=(5, ), random_state=1)

#tuning parameter
param_grid = [{'alpha': [1e-5,1e-4,1e-3,1e-2] , 'hidden_layer_sizes': [(5,),(10,),(15,),(20,)]}]
alphas = [1e-5,1e-4,1e-3,1e-2,1e-1,1,10,100,1000]
hidden_layer_sizeing = [(1, ),(5, ),(10, ),(20,),(30,),(40,),(50,),(100,),(200,)]
'''
classifier = GridSearchCV(estimator=clf, cv=cv, param_grid=param_grid)
classifier.fit(X_train, y_train.ravel())
print("Best alpha values")
print(classifier.best_estimator_.alpha)
print("Best layer values")
print(classifier.best_estimator_.hidden_layer_sizes)
'''
al = 1e-5
ls = (20,)
#debugging

title = 'Learning Curves (MLP, $\ alpha=%.6f$)' %al
estimator = MLPClassifier(solver='lbfgs',learning_rate = 'adaptive', random_state=1)
'''
plot_learning_curve(estimator, title, X_train, y_train.ravel(), cv=cv)
plt.show()

#scoring
print("classifier score")
print(classifier.score(X_test, y_test))
#print("cross classifier score")
#print(cross_val_score(classifier, X, Y))
'''
#plot validation curve
param_range = alphas
train_scores, test_scores = validation_curve(
    MLPClassifier(solver='lbfgs',learning_rate = 'adaptive', random_state=1), 
    X, Y.ravel(), param_name="alpha", param_range=param_range,
    cv=2, scoring="accuracy", n_jobs=1)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

plt.title("Validation Curve with MLP")
plt.xlabel("$\ alpha$")
plt.ylabel("Score")
plt.ylim(0.0, 1.1)
lw = 2
#param_range_tup = [int(i[0]) for i in param_range]
'''
plt.semilogx(param_range_tup, train_scores_mean, label="Training score",
             color="darkorange", lw=lw)
plt.fill_between(param_range_tup, train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.2,
                 color="darkorange", lw=lw)
plt.semilogx(param_range_tup, test_scores_mean, label="Cross-validation score",
             color="navy", lw=lw)
plt.fill_between(param_range_tup, test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std, alpha=0.2,
                 color="navy", lw=lw)
'''
plt.semilogx(param_range, train_scores_mean, label="Training score",
             color="darkorange", lw=lw)
plt.fill_between(param_range, train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.2,
                 color="darkorange", lw=lw)
plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
             color="navy", lw=lw)
plt.fill_between(param_range, test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std, alpha=0.2,
                 color="navy", lw=lw)

plt.legend(loc="best")
plt.show()
'''

clf.fit(X,Y.ravel())
Y_pred = clf.predict(X)

#print(clf.get_params())
print("")
print("##############################################")
print("")
print(classification_report(Y,Y_pred,target_names=target_names))
print("##############################################")
print("")

scores = cross_val_score(clf, X, Y.ravel(), cv=10)

print(scores)
plot_learning_curve()
plt.show()

model_name = 'MLP_model100k.sav'
pickle.dump(estimator,open(model_name,'w'))
with open(name_new_file, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(Y_pred)
csvwrite.close()
'''
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

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
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
alphas = [1e-5,1e-4,1e-3,1e-2]
hidden_layer_sizeing = [(1, ),(5, ),(10, ),(20,)]
classifier = GridSearchCV(estimator=clf, cv=cv, param_grid=param_grid)
classifier.fit(X_train, y_train.ravel())
print("Best alpha values")
print(classifier.best_estimator_.alpha)
print("Best layer values")
print(classifier.best_estimator_.hidden_layer_sizes)

#debugging
title = 'Learning Curves (MLP, $\ alpha=%.6f$)' %classifier.best_estimator_.alpha
estimator = MLPClassifier(solver='lbfgs',learning_rate = 'adaptive', alpha=classifier.best_estimator_.alpha,hidden_layer_sizes=classifier.best_estimator_.hidden_layer_sizes, random_state=1)
plot_learning_curve(estimator, title, X_train, y_train.ravel(), cv=cv)
plt.show()

#scoring
print("classifier score")
print(classifier.score(X_test, y_test))
#print("cross classifier score")
#print(cross_val_score(classifier, X, Y))



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
'''
model_name = 'MLP_model100k.sav'
pickle.dump(estimator,open(model_name,'w'))
with open(name_new_file, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(Y_pred)
csvwrite.close()
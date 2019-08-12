import pandas as pd
from sklearn import preprocessing
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import classification_report
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

dataset = np.loadtxt("dataset_array_champs_averages.csv", delimiter=",")
labels = np.loadtxt("dataset_array_labels.csv",delimiter=",")
onecount=0
zerocount = 0
for i in labels:
    if i == 1:
        onecount +=1
    elif i == 0:
        zerocount +=1
onewin = np.array((4348,60))
zerowin = np.array((4302,60))
#for i in dataset:

print("Loaded Dataset")
X_train, X_test, Y_train, Y_test = train_test_split(dataset, labels, test_size=0.30, random_state=101)
gnb = GaussianNB()
gnb.fit(X_train,Y_train)

#Logistic Regression
logmodel = LogisticRegression()

grid={"C":np.logspace(-3,3,7), "penalty":["l1","l2"]}
logmodel_cv=GridSearchCV(logmodel, grid, cv=10)
logmodel_cv.fit(X_train, Y_train)
print("Best hyperparameters: ",logmodel_cv.best_params_)
print("accuracy : ", logmodel_cv.best_score_)
logmodel_final = LogisticRegression(C=logmodel_cv.best_params_['C'], penalty=logmodel_cv.best_params_['penalty'])
logmodel_final.fit(X_train, Y_train)
score = logmodel_final.score(X_test, Y_test)

# Random Forest
# Random Search
n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10,110,num=11)]
max_depth.append(None)
min_samples_split = [2,5,10]
min_samples_leaf = [1,2,4]
bootstrap = [True, False]

random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
#RF_random = RandomizedSearchCV(estimator=RFC, param_distributions=random_grid, n_iter=100, cv=5, verbose=2, random_state=42,n_jobs=-1)
#RF_random.fit(X_train,Y_train)
#print(RF_random.best_params_)
# 500 permutations tested 51 minutes
#bestRFParams = {'n_estimators': 1600, 'min_samples_split': 10, 'min_samples_leaf': 1, 'max_features': 'sqrt', 'max_depth': 20, 'bootstrap': True}
RFC = RandomForestClassifier()
RFC_optimal = RandomForestClassifier(n_estimators=1600, min_samples_split=10, min_samples_leaf=1, max_features='sqrt',max_depth=20, bootstrap=True)

RFC.fit(X_train, Y_train)
RFC_optimal.fit(X_train,Y_train)
RFCPredictions = RFC.predict(X_test)
RFC_Optimal_predictions = RFC_optimal.predict(X_test)
scoreRFC = RFC.score(X_test,Y_test)
scoreRFC_Opt = RFC_optimal.score(X_test,Y_test)
print('Default Accuracy of {:0.2f}%'.format(100*scoreRFC),'Random Accuracy of {:0.2f}%'.format(100*scoreRFC_Opt),'Optimal random parameters improvement of {:0.2f}%.'.format(100*(scoreRFC_Opt-scoreRFC)/scoreRFC))
print('Performing Grid Search')
param_grid = {
    'bootstrap': [True],
    'max_depth':[20,30,40,50],
    'max_features':['sqrt'],
    'min_samples_leaf':[1,2,3,4],
    'min_samples_split':[10,11,12,13],
    'n_estimators':[1500,1600,1700,1800]
}
newRF = RandomForestClassifier()
rf_grid_search = GridSearchCV(estimator=newRF, param_grid=param_grid, cv=5,n_jobs=-1,verbose=2)
rf_grid_search.fit(X_train,Y_train)
bestParams = rf_grid_search.best_params_
bestGrid = rf_grid_search.best_estimator_
scoreGrid = rf_grid_search.score(X_test,Y_test)
#RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
           # max_depth=30, max_features='sqrt', max_leaf_nodes=None,
        #    min_impurity_decrease=0.0, min_impurity_split=None,
          #  min_samples_leaf=1, min_samples_split=10,
           # min_weight_fraction_leaf=0.0, n_estimators=1700, n_jobs=None,
          #  oob_score=False, random_state=None, verbose=0,
          #  warm_start=False)
          #1280 permutations tested
print('Default Accuracy of {:0.2f}%'.format(100*scoreRFC),'Random Accuracy of {:0.2f}%'.format(100*scoreRFC_Opt),
' Grid search accuracy of {:0.2f}%'.format(100*scoreGrid),
' Optimal random parameters improvement of {:0.2f}%.'.format(100*(scoreGrid-scoreRFC)/scoreRFC))



mySVM = svm.SVC(gamma='scale')
mySVM.fit(X_train,Y_train)
SVMpredictions = mySVM.predict(X_test)
logmodel.fit(X_train, Y_train)
predictions = logmodel.predict(X_test)
scoreSVM = mySVM.score(X_test,Y_test)
score = logmodel.score(X_test, Y_test)
scoreNB = gnb.score(X_test,Y_test)

print(score)
print(dataset)
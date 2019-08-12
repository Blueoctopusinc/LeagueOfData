import numpy as np
import matplotlib.pyplot as plt
plt.rc("font", size=14)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

################################# Data Imports #########################################

dataset = np.loadtxt("dataset_array_champs_averages.csv", delimiter=",")
labels = np.loadtxt("dataset_array_labels.csv", delimiter=",")

################################# Pre-Processing #######################################

le = LabelEncoder()
one_hot = OneHotEncoder(sparse=False)

df = pd.DataFrame(dataset)
df2 = pd.DataFrame(df[df.columns[0]])
df2 = pd.concat([df2,df[df.columns[6]]], axis=1)
df2 = pd.concat([df2,df[df.columns[12]]], axis=1)
df2 = pd.concat([df2,df[df.columns[18]]], axis=1)
df2 = pd.concat([df2,df[df.columns[24]]], axis=1)
df2 = pd.concat([df2,df[df.columns[30]]], axis=1)
df2 = pd.concat([df2,df[df.columns[36]]], axis=1)
df2 = pd.concat([df2,df[df.columns[42]]], axis=1)
df2 = pd.concat([df2,df[df.columns[48]]], axis=1)
df2 = pd.concat([df2,df[df.columns[54]]], axis=1)
df.drop(df.columns[[0,6,12,18,24,30,36,42,48,54]], axis=1, inplace=True)

champs_encoded = df2.apply(le.fit_transform)
one_hot.fit(champs_encoded)
one_hot_champs = one_hot.transform(champs_encoded)

one_hot_df = pd.DataFrame(one_hot_champs)
encoded_data = pd.concat([df,one_hot_df], axis=1)

#print(encoded_data)

x_train, x_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.3, random_state=101)
x_train_enc, x_test_enc, y_train_enc, y_test_enc = train_test_split(encoded_data, labels, test_size=0.3, random_state=101)

################################ Random Forest Classifier ###############################

RandomForestEnc = RandomForestClassifier()
RandomForestOpt = RandomForestClassifier(n_estimators=1800, min_samples_split=2, min_samples_leaf=1, max_features='sqrt', max_depth=50, bootstrap=True)

random_grid = {
    'n_estimators': [int(x) for x in np.linspace(start=200, stop=2000, num=10)],
    'max_features': ['auto', 'sqrt'],
    'max_depth': [int(x) for x in np.linspace(10,110, num=11)],
    'min_samples_split': [2,5,10],
    'min_samples_leaf': [1,2,4],
    'bootstrap': [True, False]
}

#RandomForestRandomized = RandomizedSearchCV(estimator=RandomForest, param_distributions=random_grid, n_iter=100, verbose=2,random_state=42, n_jobs=-1)
#RandomForestRandomized.fit(x_train,y_train)

#print(RandomForestRandomized.best_params_, RandomForestRandomized.best_score_)

RandomForestEnc.fit(x_train_enc, y_train_enc)
endScore = RandomForestEnc.score(x_test_enc, y_test_enc)

RandomForestOpt.fit(x_train, y_train)
score = RandomForestOpt.score(x_test, y_test)

print("Validation Set Score: ", score, "One-Hot encoded score: ", endScore)
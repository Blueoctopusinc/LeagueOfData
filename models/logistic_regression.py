import numpy as np
import matplotlib.pyplot as plt
plt.rc("font", size=14)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
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

print(encoded_data)

x_train, x_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.3, random_state=101)
x_train_enc, x_test_enc, y_train_enc, y_test_enc = train_test_split(encoded_data, labels, test_size=0.3, random_state=101)



################################# Logistic Regression ###################################

logmodel = LogisticRegression()

# Logistic Regression with default parameters
defaultModel = LogisticRegression()
############## GRID SEARCH ###################
# Grid Search Parameters
grid = {"C":np.logspace(-3,3,7), "penalty":["l1","l2"]}

logmodel_optimal = GridSearchCV(logmodel, grid, cv=10)
logmodel_optimal.fit(x_train_enc,y_train_enc)

opt_score = logmodel_optimal.score(x_test_enc,y_test_enc)

# Fit and train default model on one-hot encoded values w/ accuracy on validation set
defaultModel.fit(x_train_enc,y_train_enc)
default_score_encoded = defaultModel.score(x_test_enc,y_test_enc)

# Fit and train default model on unencoded values w/ accuracy on validation set
defaultModel.fit(x_train,y_train)
default_score_unencoded = defaultModel.score(x_test,y_test)


print("Default unencoded score: " , default_score_unencoded, " Default score encoded: ", default_score_encoded ,
      " Grid Searched Parameters Model score: ", opt_score)

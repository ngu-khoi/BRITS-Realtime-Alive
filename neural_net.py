import xgboost as xgb
import numpy as np
import os
import csv
model_name = 'brits'

impute = np.load('./{}_data.npy'.format(model_name)).reshape(-1, 48*35)
print(impute.shape)

label = np.load('./{}_label.npy'.format(model_name)).reshape(-1,)
print(label.shape)

data = np.nan_to_num(impute)
n_train = 3000

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_auc_score

auc = []

for i in range(10):
    model = MLPClassifier(random_state=1, max_iter=300).fit(data[:n_train], label[:n_train])
    pred = model.predict_proba(data[n_train:])

    auc.append(roc_auc_score(label[n_train:].reshape(-1,), pred[:, 1].reshape(-1, )))
print(pred)
print(np.mean(auc))
#Create outfile
outfile = "./result/data2.csv"
print("Processing data")
x = open(outfile, "a", newline='')
csv_writer = csv.writer(x)
#Write header + patient specific classifiers
csv_writer.writerow([pred[7][0], pred[7][1], np.mean(auc)] )
x.close()
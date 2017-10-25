# -*- coding: utf-8 -*-

import pandas as pd
import sklearn_pandas
import sklearn2pmml
from sklearn import preprocessing
from sklearn import svm
from sklearn import pipeline

xxx=[]
data=pd.read_csv("./01_16_ip_1_feature.txt")
mapper=sklearn_pandas.DataFrameMapper([
    ([i], preprocessing.StandardScaler()) for i in data.columns
    ])
train=mapper.fit_transform(data)

pipeline_estimator=pipeline.Pipeline([
    ('estimator',svm.OneClassSVM(nu=0.015, kernel="rbf",gamma=0.04))
    ])
pipeline_estimator.fit(train)
data1 = pd.read_csv("./17_ip_1_feature.txt")
train1 = mapper.transform(data1)
pred_test = pipeline_estimator.predict(train1)
for i in range(len(pred_test)):
    if pred_test[i] != 1:
        xxx.append(i)

#xxx = pred_test[pred_test == -1]

#sklearn2pmml.sklearn2pmml(pipeline_estimator,mapper,"./track_model.pmml", with_repr=True,debug=True)


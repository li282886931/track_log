from sklearn import svm
import numpy as np
from sklearn.cross_validation import train_test_split

data = np.loadtxt("E://1001_1010_ip_3_feature.txt")

X_train, X_test, train_y, test_y = train_test_split(data, 1, test_size=0.2, random_state=0)
clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
clf.fit(X_train)
#y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)

print float(y_pred_test[y_pred_test == -1].size) / y_pred_test.size
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV,train_test_split
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

import time
start_time = time.time()



X_public = np.load('X_public.npy')
y_public = np.load('y_public.npy')
X_eval = np.load('X_eval.npy')

print('X_public_npy shape:\t' + str(X_public.shape))
print('y_public.npy shape:\t' + str(y_public.shape))
print('X_eval.npy shape:\t' + str(X_eval.shape))

enc1 = LabelEncoder()
for i in range(len(X_public)):
    for j in range(len(X_public[i])):
        if type(X_public[i, j]) == str:
            label_encoder1 = enc1.fit(X_public[:, j])
            integer_classes1 = label_encoder1.transform(label_encoder1.classes_)
            X_public[:, j] = label_encoder1.transform(X_public[:, j])
            X_eval[:, j] = label_encoder1.transform(X_eval[:, j])

for i in range(len(X_public[0])):
    num=X_public[:, i]
    num=np.array(num)
    average = np.argmax(num[~pd.isnull(num)])
    num[pd.isnull(num)]=average
    X_public[:, i]=num
    num = X_eval[:, i]
    num = np.array(num)
    average = np.argmax(num[~pd.isnull(num)])
    num[pd.isnull(num)] = average
    X_eval[:, i] = num

X_train, X_test, y_train, y_test = train_test_split(X_public.astype(float), y_public.astype(float), test_size=0.20, random_state=50)


def rfr_model(X, y):
    print("Start Grid-Search")
    gsc = GridSearchCV(
        estimator= AdaBoostRegressor(),
        param_grid={
            'random_state': (50, 40, 8),
            'n_estimators': (100, 500, 1000),
            'loss': ('linear', 'square', 'exponential')

        },
        cv=5, scoring='explained_variance', verbose=5, n_jobs=-1)

    grid_result = gsc.fit(X, y)
    best_params = grid_result.best_params_

    print(best_params)

    return best_params


#best_params = rfr_model(X_public, y_public)
print("Start fit")
#abr = AdaBoostRegressor(n_estimators=best_params['n_estimators'], random_state=best_params['random_state'], loss=best_params['loss'])
abr = AdaBoostRegressor(n_estimators=1000, random_state=8, loss='square')
abr.fit(X_train, y_train)
print("Accuracy on training set: {:6f}\t".format(abr.score(X_train, y_train)))
print("Accuracy on test set: {:6f}\t".format(abr.score(X_test, y_test)))


y_predict = abr.predict(X_train)
np.save('y_predikcia', y_predict)
print("--- {:1f} seconds ---" .format(time.time() - start_time))


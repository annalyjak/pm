import src.read_netcdf as reader
import pandas as pd
from statsmodels.tsa.ar_model import AR
import numpy as np
from pandas import Series
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error


def predict(coef, history):
	yhat = coef[0]
	for i in range(1, len(coef)):
		yhat += coef[i] * history[-i]
	return yhat
# create a difference transform of the dataset


data = reader.read_nsidc_all('north', '1979', '2017')

trainData = [x for x in data.Mean[1:455] if x is not None]  # data.Mean[-350:-12]
trainData = np.nan_to_num(trainData)
trainData = pd.Series(trainData)
# print(len(trainData))
testData = []
for i in range(455,467):
    testData.append(data.Mean[i])
model = AR(np.asarray(trainData))
model_fit = model.fit(maxlag=6, disp=False)
window = model_fit.k_ar
coef = model_fit.params

history = [trainData.iloc[i] for i in range(len(trainData))]
predictions = list()
for t in range(len(testData)):
    print (t)
    yhat = predict(coef, history)
    obs = testData[t]
    predictions.append(yhat)
    history.append(obs)
error = mean_squared_error(testData, predictions)
print('Test MSE: %.3f' % error)

print(testData)
# plot
pyplot.plot(testData)
pyplot.plot(predictions, color='red')
pyplot.show()

import warnings
import itertools
from datetime import datetime
import numpy as np
import pandas as pd
from pylab import rcParams
import matplotlib.pyplot as plt
import statsmodels.api as sm


def print_trend_seasonality_and_noise(y, title):
    rcParams['figure.figsize'] = 18, 8
    decomposition = sm.tsa.seasonal_decompose(y, model='additive', freq=12)
    fig = decomposition.plot()
    # plt.title("Trendy, sezonowość i noise - " + title)
    plt.savefig('../plots/ostateczne/' + "Trendy, sezonowość i noise - " + title + '.png', dpi=100)
    plt.show()


def ARIMA(y, title):
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    # print('Examples of parameter combinations for Seasonal ARIMA...')
    # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
    # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
    # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
    # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)
                results = mod.fit()
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue

    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=(1, 1, 1),
                                    seasonal_order=(1, 1, 0, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    # print(results.summary().tables[1])

    # DIAGNOSTIC IF NORMAL
    # results.plot_diagnostics(figsize=(16, 8))
    # plt.savefig('../plots/ostateczne/' + "Badanie rozkładu zmiennej: " + title + '.png', dpi=100)
    # plt.show()

    #
    pred = results.get_prediction(start=len(y)-12, dynamic=False)
    pred_ci = pred.conf_int()
    # ax = y['1979':].plot(label='observed') # Big chart
    ax = y['2005':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel(title)
    plt.legend()
    # plt.savefig('../plots/ostateczne/' + "Predykcja dla " + title + '.png', dpi=100)
    # plt.savefig('../plots/ostateczne/' + "Predykcja dla " + title + ' - mniejszy wykres.png', dpi=100)
    plt.show()

    y_forecasted = pred.predicted_mean
    y_truth = y[len(y)-12:]
    mse = ((y_forecasted - y_truth) ** 2).mean()
    print(title + ' The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
    print(title + ' The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

    # Next preditions:
    pred_uc = results.get_forecast(steps=100)
    pred_ci = pred_uc.conf_int()
    ax = y[len(y)-24:len(y)].plot(label='observed', figsize=(14, 7))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Furniture Sales')
    plt.legend()
    plt.savefig('../plots/ostateczne/' + "100 wartości do przodu - " + title + '.png', dpi=100)
    plt.show()
from netCDF4 import Dataset
import glob
from pandas.plotting import register_matplotlib_converters
from src.charts_generator import plot_data2, plot_histogram, plot_model
from src.data_frame_creator import create_dataframes, create_dataframes_temp
from src.model_creator import create_model, linear_regression_model, predict_using_model, svr_model, svr_lin_model
import numpy as np


def read_nsidc_all(path, year_start, year_end):
    alldataset = []
    year = int(year_start)
    while year <= int(year_end):
        for filename in glob.iglob('../data/' + path + '/monthly/*' + str(year) + '*.nc'):
            dataset = Dataset(filename)
            date = filename[len(filename)-16:len(filename)-10]
            alldataset.append([dataset, date])
        year = year + 1

    return create_dataframes(alldataset)


def read_nsidc_temp(path):
    alldataset = []
    for filename in glob.iglob('../data/' + path + '/*.nc'):
        dataset = Dataset(filename, 'r')
        date = filename[len(filename) - 13:len(filename) - 7]
        print(date)
        alldataset.append([dataset, date])

    return create_dataframes_temp(alldataset)


def read_year(path, year):
    alldataset = []
    count = 1
    while count < 10:
        for filename in glob.iglob('../data/' + year + '/0' + str(count) + '/*' + path + '*.nc'):
            dataset = Dataset(filename)
            alldataset.append(dataset)
        count = count + 1
    count = 10
    while count <= 12:
        for filename in glob.iglob('../data/' + year + '/' + str(count) + '/*' + path + '*.nc'):
            dataset = Dataset(filename)
            alldataset.append(dataset)
        count = count + 1

    return create_dataframes(alldataset)


def plot_year(sorted_df, path, year):
    title1 = path + ': Ice conc in ' + year
    plot_data(sorted_df, title1)
    title2 = path + ': Histogram ' + year
    plot_histogram(sorted_df, title2)


def plot_data(path, year_start, year_end):
    sorted_df = read_nsidc_all(path, year_start, year_end)
    title1 = path + ': Ice conc in years: ' + year_start + ' - ' + year_end
    plot_data2(sorted_df, title1)
    title2 = path + ': Histogram ' + year_start + ' - ' + year_end
    plot_histogram(sorted_df, title2)


def split_into_sets(data):
    x_labels = [str(x) for x in data.YearMonth]
    x = list(zip(range(0, len(data.YearMonth))))   # data.YearMonth
    y = list(data.NASA) # MUST BE NOT NAN AND INF
    x_train = x[:30]
    y_train = y[:30]
    x_train_label = x_labels[:30]
    x_test = x[30:]
    y_test = y[30:]
    x_test_label = x_labels[30:]
    return x_train, y_train, x_test, y_test, x_train_label, x_test_label


def model_procedure(data):
    x_train, y_train, x_test, y_test, x_train_l, x_test_l = split_into_sets(data)
    # print(len(x_train))
    # print(len(y_train))
    # print(np.any(np.isnan(x_train))) # and gets False
    # print(np.all(np.isfinite(x_train)))  # and gets True
    # print(np.any(np.isnan(y_train)))  # and gets False
    # print(np.all(np.isfinite(y_train)))  # and gets True
    regr = linear_regression_model(x_train, y_train)
    y_pred = predict_using_model(regr, x_test)
    plot_model(regr, x_test, y_test, y_pred, x_train_l, x_test_l)


def main():
    register_matplotlib_converters()
    # info_data_nsidc()
    # plot_year(data, 'north', '1987')

    # max -> 1978 - 2017
    # PLOT ALL DATA:
    # plot_data('north', '1979', '2017')
    # plot_data('south', '1979', '2017')

    # get data:
    # data = read_nsidc_all('north', '1985', '1990')
    # model_procedure(data)

    read_nsidc_temp('temp')
    # info_data_temperature()



if __name__ == "__main__":
  main()
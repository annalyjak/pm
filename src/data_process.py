from netCDF4 import Dataset
import numpy as np
from datetime import datetime
import glob
import matplotlib.pyplot as plt
import pandas as pd


def start_info_print():
    nc_file_path_1 = '../data/2010/01/ice_conc_nh_ease2-250_cdr-v2p0_201001011200.nc'
    nc_file_path_2 = '../data/2010/01/ice_conc_nh_ease2-250_cdr-v2p0_201001021200.nc'

    dataset = Dataset(nc_file_path_1)

    # To check what kind of keys we have
    print(dataset.variables.keys())

    # check type of attributes:
    print(dataset.variables['Lambert_Azimuthal_Grid'])
    print(dataset.variables['time'])
    print(dataset.variables['time_bnds'])
    print(dataset.variables['xc'])
    print(dataset.variables['yc'])
    print(dataset.variables['lat'])
    print(dataset.variables['lon'])
    print(dataset.variables['ice_conc'])
    # print(dataset.variables['standard_error'])
    print(dataset.variables['total_standard_error'])
    print(dataset.variables['smearing_standard_error'])
    print(dataset.variables['status_flag'])

    dataset2 = Dataset(nc_file_path_2)
    print(dataset2.variables['Polar_Stereographic_Grid'])
    print(dataset2.variables['algorithm_standard_error'])


def calculate_mean(dataset):
    timestamp = None
    mean = None
    std = None
    ice = dataset.variables['ice_conc']
    date = dataset.variables['time']
    for d in date:
        timestamp = d
    for i in ice:
        mean = np.mean(i)
        std = np.std(i, ddof=1)  # odchylenie standardowe próbki
    return timestamp, mean, std


def get_all_dates_and_means(datasets):
    dataframes = []
    for dataset in datasets:
        d, m, s = calculate_mean(dataset)
        dataframes.append([datetime.fromtimestamp(d), m, s, int(d)])
    return dataframes


def plot_data(sorted_df, title):
    plt.plot(sorted_df.Datatime, sorted_df.Mean, 'm*')
    plt.ylabel('ice conc')
    plt.xlabel('date')
    plt.xticks(rotation=20)
    plt.title(title)
    plt.savefig('../plots/' + title + '.png', dpi=100)
    plt.show()


def plot_histogram(sorted_df, title):
    plt.hist(sorted_df.Mean, density=1, facecolor='m', alpha=0.75)
    plt.title(title)
    plt.grid(True)
    plt.savefig('../plots/' + title + '.png', dpi=100)
    plt.show()


#TODO fix error
def plot_boxplot(sorted_df):
    plt.boxplot(sorted_df)
    plt.show()


def create_dataframes(datasets):
    data = get_all_dates_and_means(datasets)
    df = pd.DataFrame(data, columns=['Datatime', 'Mean', 'Std', 'Timestamp'])
    sorted_df = df.sort_values(by=['Timestamp'])
    print(sorted_df)
    return sorted_df


def read_and_plot_month(path, year, month):
    alldataset = []
    for filename in glob.iglob('../data/' + year + '/' + month + '/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)

    sorted_df = create_dataframes(alldataset)

    title1 = path + ': Ice conc in ' + year + '-' + month
    plot_data(sorted_df, title1)
    # plot_boxplot(sorted_df)


def read_and_plot_year(path, year):
    alldataset = []
    for filename in glob.iglob('../data/' + year + '/01/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/02/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/03/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/04/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/05/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/06/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/07/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/08/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/09/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/10/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/11/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)
    for filename in glob.iglob('../data/' + year + '/12/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)

    sorted_df = create_dataframes(alldataset)

    title1 = path + ': Ice conc in ' + year
    plot_data(sorted_df, title1)
    title2 = path + ': Histogram ' + year
    plot_histogram(sorted_df, title2)
    # plot_boxplot(sorted_df)


def main():
    year = '2010'
    read_and_plot_month('nh', year, '01')
    read_and_plot_month('sh', year, '01')
    read_and_plot_month('nh', year, '02')
    read_and_plot_month('sh', year, '02')
    read_and_plot_month('nh', year, '03')
    read_and_plot_month('sh', year, '03')
    read_and_plot_month('nh', year, '04')
    read_and_plot_month('sh', year, '04')
    read_and_plot_month('nh', year, '05')
    read_and_plot_month('sh', year, '05')
    read_and_plot_month('nh', year, '06')
    read_and_plot_month('sh', year, '06')
    read_and_plot_month('nh', year, '07')
    read_and_plot_month('sh', year, '07')
    read_and_plot_month('nh', year, '08')
    read_and_plot_month('sh', year, '08')
    read_and_plot_month('nh', year, '09')
    read_and_plot_month('sh', year, '09')
    read_and_plot_month('nh', year, '10')
    read_and_plot_month('sh', year, '10')
    read_and_plot_month('nh', year, '11')
    read_and_plot_month('sh', year, '11')
    read_and_plot_month('nh', year, '12')
    read_and_plot_month('sh', year, '12')

    read_and_plot_year('nh', year='2010')
    read_and_plot_year('sh', year='2010')


if __name__== "__main__":
  main()
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


def plot_data(path, sorted_df):
    plt.plot(sorted_df.Datatime, sorted_df.Mean, 'm*')
    plt.ylabel('ice conc')
    plt.xlabel('date')
    plt.xticks(rotation=20)
    day = sorted_df.Datatime[0]
    title = path + ': Ice conc in ' + str(day.year) + '.' + str(day.month)
    plt.title(title)
    plt.show()


#TODO change to good method
def plot_histogram(sorted_df):
    # the histogram of the data
    n, bins, patches = plt.hist(sorted_df.Mean, density=1, facecolor='m', alpha=0.75)
    plt.title('Histogram')
    plt.grid(True)
    plt.show()


#TODO fix error
def plot_boxplot(sorted_df):
    plt.boxplot(sorted_df)
    plt.show()


def create_dataframes(datasets):
    data = get_all_dates_and_means(datasets)
    df = pd.DataFrame(data, columns=['Datatime', 'Mean', 'Std', 'Timestamp'])
    # print(df)
    # for i in df:
    #     print(df.Timestamp)
    sorted_df = df.sort_values(by=['Timestamp'])
    print(sorted_df)
    return sorted_df


def read_and_plot_path(path):
    alldataset = []
    for filename in glob.iglob('../data/2010/01/' + path + '/*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)

    sorted_df = create_dataframes(alldataset)

    plot_data(path, sorted_df)
    # plot_histogram(sorted_df)
    # plot_boxplot(sorted_df)


def main():
    read_and_plot_path('nh')
    read_and_plot_path('sh')


if __name__== "__main__":
  main()
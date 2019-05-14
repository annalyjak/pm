from netCDF4 import Dataset
import numpy as np
from datetime import datetime
import glob
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters


def info_data_temperature():
    nc_file = '../data/temp/MERRA300.prod.assim.instM_3d_asm_Cp.200712.hdf.nc'
    dataset = Dataset(nc_file)

    # To check what kind of keys we have
    print(dataset.variables.keys())
    print(dataset.variables['T'])
    print(dataset.variables['Height'])
    print(dataset.variables['TIME'])
    print(dataset.variables['XDim'])
    print(dataset.variables['YDim'])


def info_data_nsidc():
    nc_file = '../data/north/monthly/seaice_conc_monthly_nh_f08_198708_v03r01.nc'
    dataset = Dataset(nc_file)

    # To check what kind of keys we have
    print(dataset.variables.keys())
    print(dataset.variables['seaice_conc_monthly_cdr'])
    print(dataset.variables['stdev_of_seaice_conc_monthly_cdr'])
    print(dataset.variables['melt_onset_day_seaice_conc_monthly_cdr'])
    print(dataset.variables['qa_of_seaice_conc_monthly_cdr'])
    print(dataset.variables['goddard_merged_seaice_conc_monthly'])
    print(dataset.variables['goddard_nt_seaice_conc_monthly'])
    print(dataset.variables['goddard_bt_seaice_conc_monthly'])
    print(dataset.variables['time'])
    print(dataset.variables['ygrid'])
    print(dataset.variables['xgrid'])
    print(dataset.variables['latitude'])
    print(dataset.variables['longitude'])
    for i in dataset.variables['time']:
        print(i)

    nc_file = '../data/north/monthly/seaice_conc_monthly_nh_f08_198709_v03r01.nc'
    dataset = Dataset(nc_file)
    for i in dataset.variables['time']:
        print(i)


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


def calculate_mean2(dataset):
    timestamp = None
    mean = None
    std = None
    ice1 = dataset.variables['goddard_merged_seaice_conc_monthly']
    # Goddard Edited Climate Data Record of Passive Microwave Monthly Northern Hemisphere Sea Ice Concentration
    ice2 = dataset.variables['goddard_nt_seaice_conc_monthly']
    # Passive Microwave Monthly Northern Hemisphere Sea Ice Concentration by NASA Team algorithm with Goddard QC
    ice3 = dataset.variables['goddard_bt_seaice_conc_monthly']
    # Passive Microwave Monthly Northern Hemisphere Sea Ice Concentration by Bootstrap algorithm with Goddard QC
    date = dataset.variables['time']
    for d in date:
        timestamp = d
    for i in ice1:
        mean1Goddard = np.mean(i)
        std = np.std(i, ddof=1)  # odchylenie standardowe próbki
    for i in ice2:
        mean2NASA = np.mean(i)
    for i in ice3:
        mean3Bootstrap = np.mean(i)
    return timestamp, mean1Goddard, std, mean2NASA, mean3Bootstrap


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


def get_all_dates_and_means2(datasets):
    dataframes = []
    for dataset, date in datasets:
        d, m, s, m2, m3 = calculate_mean2(dataset)
        d8 = datetime.fromtimestamp(d)
        d8 = d8.replace(year=int(date[0:4]), month=int(date[4:len(date)]))
        dataframes.append([d8, m, s, m2, m3, int(date)])
    return dataframes


def get_all_dates_and_means(datasets):
    dataframes = []
    for dataset in datasets:
        d, m, s = calculate_mean(dataset)
        d8 = datetime.fromtimestamp(d)
        d8 = d8.replace(year=int(d8.year + 8))
        dataframes.append([d8, m, s, int(d), str(d)])
    return dataframes


def plot_data2(sorted_df, title):
    plt.plot(sorted_df.Datatime, sorted_df.Mean, 'm')
    plt.plot(sorted_df.Datatime, sorted_df.NASA, 'g')
    plt.plot(sorted_df.Datatime, sorted_df.Bootstrap, 'b')
    plt.ylabel('ice conc')
    plt.xlabel('date')
    plt.xticks(rotation=20)
    plt.title(title)
    plt.legend(['Mean', 'NASA', 'Bootstrap'], loc='upper right')
    plt.savefig('../plots/' + title + '.png', dpi=100)
    plt.show()


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


def create_dataframes2(datasets):
    data = get_all_dates_and_means2(datasets)
    # Goddard Edited Climate Data Record of Passive Microwave Monthly Northern Hemisphere Sea Ice Concentration
    df = pd.DataFrame(data, columns=['Datatime', 'Mean', 'Std', 'NASA', 'Bootstrap', 'YearMonth'])
    sorted_df = df.sort_values(by=['YearMonth'])
    print(sorted_df)
    return sorted_df


def create_dataframes(datasets):
    data = get_all_dates_and_means(datasets)
    df = pd.DataFrame(data, columns=['Datatime', 'Mean', 'Std', 'Timestamp'])
    sorted_df = df.sort_values(by=['Timestamp'])
    print(sorted_df)
    return sorted_df


def read_and_plot_nsidc(path, year):
    alldataset = []
    for filename in glob.iglob('../data/' + path + '/monthly/*' + year + '*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)

    sorted_df = create_dataframes2(alldataset, year, 1)

    title1 = path + ': Ice conc in '
    plot_data2(sorted_df, title1)
    # plot_boxplot(sorted_df)


def read_and_plot_month(path, year, month):
    alldataset = []
    for filename in glob.iglob('../data/' + year + '/' + month + '/*' + path + '*.nc'):
        dataset = Dataset(filename)
        alldataset.append(dataset)

    sorted_df = create_dataframes(alldataset)

    title1 = path + ': Ice conc in ' + year + '-' + month
    plot_data(sorted_df, title1)
    # plot_boxplot(sorted_df)


def read_and_plot_year(path, year):
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

    sorted_df = create_dataframes(alldataset)

    title1 = path + ': Ice conc in ' + year
    plot_data(sorted_df, title1)
    title2 = path + ': Histogram ' + year
    plot_histogram(sorted_df, title2)
    # plot_boxplot(sorted_df)


def read_and_plot_all_years(path, year_start, year_end):
    alldataset = []
    year = int(year_start)
    while year <= int(year_end):
        count = 1
        while count < 10:
            for filename in glob.iglob('../data/' + str(year) + '/0' + str(count) + '/*' + path + '*.nc'):
                dataset = Dataset(filename)
                alldataset.append(dataset)
            count = count + 1
        count = 10
        while count <= 12:
            for filename in glob.iglob('../data/' + str(year) + '/' + str(count) + '/*' + path + '*.nc'):
                dataset = Dataset(filename)
                alldataset.append(dataset)
            count = count + 1
        year = year + 1

    sorted_df = create_dataframes(alldataset)

    title1 = path + ': Ice conc'
    plot_data(sorted_df, title1)
    title2 = path + ': Histogram'
    plot_histogram(sorted_df, title2)
    # plot_boxplot(sorted_df)


def read_and_plot_nsidc_all(path, year_start, year_end):
    alldataset = []
    year = int(year_start)
    while year <= int(year_end):
        for filename in glob.iglob('../data/' + path + '/monthly/*' + str(year) + '*.nc'):
            dataset = Dataset(filename)
            date = filename[len(filename)-16:len(filename)-10]
            alldataset.append([dataset, date])
        year = year + 1

    sorted_df = create_dataframes2(alldataset)

    title1 = path + ': Ice conc in years: ' + year_start + ' - ' + year_end
    plot_data2(sorted_df, title1)
    title2 = path + ': Histogram ' + year_start + ' - ' + year_end
    plot_histogram(sorted_df, title2)
    # plot_boxplot(sorted_df)


def main():
    register_matplotlib_converters()
    year = '2000'
    # read_and_plot_month('nh', year, '01')
    # read_and_plot_month('sh', year, '01')
    # read_and_plot_month('nh', year, '02')
    # read_and_plot_month('sh', year, '02')
    # read_and_plot_month('nh', year, '03')
    # read_and_plot_month('sh', year, '03')
    # read_and_plot_month('nh', year, '04')
    # read_and_plot_month('sh', year, '04')
    # read_and_plot_month('nh', year, '05')
    # read_and_plot_month('sh', year, '05')
    # read_and_plot_month('nh', year, '06')
    # read_and_plot_month('sh', year, '06')
    # read_and_plot_month('nh', year, '07')
    # read_and_plot_month('sh', year, '07')
    # read_and_plot_month('nh', year, '08')
    # read_and_plot_month('sh', year, '08')
    # read_and_plot_month('nh', year, '09')
    # read_and_plot_month('sh', year, '09')
    # read_and_plot_month('nh', year, '10')
    # read_and_plot_month('sh', year, '10')
    # read_and_plot_month('nh', year, '11')
    # read_and_plot_month('sh', year, '11')
    # read_and_plot_month('nh', year, '12')
    # read_and_plot_month('sh', year, '12')
    # read_and_plot_year('nh', year=year)
    # read_and_plot_year('sh', year=year)

    # read_and_plot_all_years('nh', '1985', '1990')

    # NEW DATASET:    # info_data_nsidc()
    # read_and_plot_nsidc('north', '1987')
    # max -> 1978 - 2017
    read_and_plot_nsidc_all('north', '1979', '2017')
    read_and_plot_nsidc_all('south', '1979', '2017')


if __name__== "__main__":
  main()
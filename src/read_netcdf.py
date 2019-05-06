from netCDF4 import Dataset
import glob
from pandas.plotting import register_matplotlib_converters
from src.charts_generator import plot_data2, plot_histogram
from src.data_frame_creator import create_dataframes


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


def main():
    register_matplotlib_converters()
    # info_data_nsidc()
    # plot_year(data, 'north', '1987')

    # max -> 1978 - 2017
    # PLOT ALL DATA:
    plot_data('north', '1979', '2017')
    plot_data('south', '1979', '2017')

    # get data:
    data = read_nsidc_all('north', '1979', '2017')


if __name__ == "__main__":
  main()
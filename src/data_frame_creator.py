import numpy as np
from datetime import datetime
import pandas as pd


def create_temp_frames(dataset):
    temperature_analysis = dataset.variables['T']
    Height = dataset.variables['Height']
    date = dataset.variables['TIME']
    for t in temperature_analysis:
        temperature = np.mean(t)
    return date, temperature, temperature - 273.15


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


def get_all_temperatures_mean(datasets):
    dataframes = []
    for dataset, date in datasets:
        a1, a2, a3 = create_temp_frames(dataset)
        d8 = datetime(year=int(date[0:4]), month=int(date[4:len(date)]), day=1)
        # d8 = d8.replace(year=int(date[0:4]), month=int(date[4:len(date)]))
        dataframes.append([d8, a2, a3, int(date), str(date)])
    return dataframes


def get_all_dates_and_means2(datasets):
    dataframes = []
    for dataset, date in datasets:
        d, m, s, m2, m3 = calculate_mean2(dataset)
        d8 = datetime.fromtimestamp(d)
        d8 = datetime(year=int(date[0:4]), month=int(date[4:len(date)]), day=1)   # d8.replace(year=int(date[0:4]), month=int(date[4:len(date)]), day=1)
        dataframes.append([d8, m, s, m2, m3, int(date)])
    return dataframes


def create_dataframes(datasets):
    data = get_all_dates_and_means2(datasets)
    # Goddard Edited Climate Data Record of Passive Microwave Monthly Northern Hemisphere Sea Ice Concentration
    df = pd.DataFrame(data, columns=['Datatime', 'Mean', 'Std', 'NASA', 'Bootstrap', 'YearMonth'])
    sorted_df = df.sort_values(by=['YearMonth'])
    print(sorted_df)
    return sorted_df


def create_dataframes_temp(datasets):
    data = get_all_temperatures_mean(datasets)
    # Goddard Edited Climate Data Record of Passive Microwave Monthly Northern Hemisphere Sea Ice Concentration
    df = pd.DataFrame(data, columns=['Datatime', 'TempK', 'TempCelc', 'YearMonth', 'YearMonthStr'])
    sorted_df = df.sort_values(by=['YearMonth'])
    print(sorted_df)
    return sorted_df
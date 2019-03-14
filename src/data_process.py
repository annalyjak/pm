from netCDF4 import Dataset

nc_file_path_1 = '../data/order3/2009-2015/ice_conc_nh_ease-125_reproc_201501011200.nc'
nc_file_path_2 = '../data/order3/2009-2015/ice_conc_nh_polstere-100_reproc_201501011200.nc'
nc_file_path_3 = '../data/order3/2009-2015/ice_conc_sh_ease-125_reproc_201501011200.nc'
nc_file_path_4 = '../data/order3/2009-2015/ice_conc_sh_polstere-100_reproc_201501011200.nc'

nc_file2_path_1 = '../data/order3/1987-2009/ice_conc_nh_ease-125_reproc_200812311200.nc'
nc_file2_path_2 = '../data/order3/1987-2009/ice_conc_nh_polstere-100_reproc_200812311200.nc'
nc_file2_path_3 = '../data/order3/1987-2009/ice_conc_sh_ease-125_reproc_200812311200.nc'
nc_file2_path_4 = '../data/order3/1987-2009/ice_conc_sh_polstere-100_reproc_200812311200.nc'

dataset = Dataset(nc_file_path_1)

# To check what kind of keys we have
print(dataset.variables.keys())
# print(dataset.dimensions['time'])

# check type of attributes:
print(dataset.variables['Lambert_Azimuthal_Grid'])
print(dataset.variables['time'])
print(dataset.variables['time_bnds'])
print(dataset.variables['xc'])
print(dataset.variables['yc'])
print(dataset.variables['lat'])
print(dataset.variables['lon'])
print(dataset.variables['ice_conc'])
print(dataset.variables['standard_error'])
print(dataset.variables['smearing_standard_error'])
print(dataset.variables['status_flag'])
print(dataset.variables['status_flag'])

dataset2 = Dataset(nc_file_path_2)
print(dataset2.variables.keys())
print(dataset2.variables['Polar_Stereographic_Grid'])
print(dataset2.variables['time'])
print(dataset2.variables['time_bnds'])
print(dataset2.variables['xc'])
print(dataset2.variables['yc'])
print(dataset2.variables['lat'])
print(dataset2.variables['lon'])
print(dataset2.variables['ice_conc'])
print(dataset2.variables['standard_error'])
print(dataset2.variables['smearing_standard_error'])
print(dataset2.variables['algorithm_standard_error'])
print(dataset2.variables['status_flag'])
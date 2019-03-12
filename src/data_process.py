from netCDF4 import Dataset

nc_file_path = '../data/order2/S-OSI_-NOR_-MULT-GL_SH_TYPEn_-201903011200Z.nc'

dataset = Dataset(nc_file_path)

# To check what kind of keys we have
print(dataset.variables.keys())
print(dataset.dimensions['time'])

# check type of attributes:
print(dataset.variables['Polar_Stereographic_Grid'])
print(dataset.variables['time'])
print(dataset.variables['time_bnds'])
print(dataset.variables['xc'])
print(dataset.variables['yc'])
print(dataset.variables['lat'])
print(dataset.variables['lon'])
print(dataset.variables['ice_type'])
print(dataset.variables['confidence_level'])
print(dataset.variables['status_flag'])


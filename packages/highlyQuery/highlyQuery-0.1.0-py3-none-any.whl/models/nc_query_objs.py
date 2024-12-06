"""
格点参考对象
@Time    : 2024/8/10 17:53
@Author  : YueJiang
@File    : nc_query_objs.py
@Software: PyCharm
"""
import xarray as xr
import utils.common_util as c_util
import consts.common_vars as var
from pathlib import Path


class BaseNcQueryObj(object):
    def __init__(self, nc_path_abs, min_lat=None, max_lat=None, min_lon=None, max_lon=None):
        self.max_lon = max_lon
        self.min_lon = min_lon
        self.max_lat = max_lat
        self.min_lat = min_lat
        self.nc_path_abs = nc_path_abs

    def get_ds(self):
        nc_files = self.nc_path_abs.split(',')
        if len(nc_files) == 1:
            if not Path(nc_files[0]).is_file():
                raise FileNotFoundError('File does not exist or directory')
            return xr.open_dataset(self.nc_path_abs)
        else:
            nc_files = [path for path in nc_files if Path(path).is_file()]
            if len(nc_files) == 0:
                raise FileNotFoundError('No valid files available')
            return xr.open_mfdataset(nc_files, combine='nested', concat_dim='time')

    def get_sel_lat_lon_ds(self, ):
        ds = self.get_ds()
        if c_util.check_none(self.min_lat, self.max_lat, self.min_lon, self.max_lon):
            return ds
        coord_vars = list(ds.coords)
        if var.LAT in coord_vars and var.LON in coord_vars:
            ds = ds.sortby(variables=var.LAT)
            return ds.sel(lat=slice(self.min_lat, self.max_lat), lon=slice(self.min_lon, self.max_lon))
        elif var.LATITUDE in coord_vars and var.LONGITUDE in coord_vars:
            ds = ds.sortby(variables=var.LATITUDE)
            return ds.sel(latitude=slice(self.min_lat, self.max_lat), longitude=slice(self.min_lon, self.max_lon))
        else:
            raise ValueError('latitude and longitude variables name not found!')

    def get_sel_time_ds(self, begin_time: str = None, end_time: str = None):
        ds = self.get_sel_lat_lon_ds()
        if c_util.check_none(begin_time, end_time):
            return ds
        if var.TIME in list(ds.coords):
            ds = self.get_sel_lat_lon_ds()
            ds = ds.sortby(variables=var.TIME)
            ds = ds.sel(time=slice(begin_time, end_time))
            return ds
        else:
            raise ValueError('time variable name not found!')

    def get_da(self, ds: xr.Dataset = None, var_key: str = None):
        if ds is None:
            ds = self.get_sel_lat_lon_ds()
            if var_key is None:
                var_key = list(ds)[0]
        else:
            if var_key is None:
                var_key = list(ds)[0]
        return ds[var_key]

    def get_sel_time_da(self, ds: xr.Dataset = None, var_key: str = None, begin_time: str = None, end_time: str = None):
        if ds is None:
            ds = self.get_sel_time_ds(begin_time, end_time)
            if var_key is None:
                var_key = list(ds)[0]
        else:
            if c_util.check_none(begin_time, end_time):
                return self.get_da(ds, var_key)
            ds = ds.sortby(variables=var.TIME)
            ds = ds.sel(time=slice(begin_time, end_time))
            if var_key is None:
                var_key = list(ds)[0]
        return ds[var_key]

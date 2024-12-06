"""
nc查询工具类
@Date    : 2024/11/23
@Author  : YueJiang
@File    : nc_query_util.py
@Software: PyCharm  
"""
import numpy as np
import pandas as pd
import xarray as xr
import consts.common_vars as var


def trans_data_nan(values, nodata=-999.0, decimals=2):
    """
    处理数据中的nan值 转换为nodata
    :param nodata: 无效值 默认-999.0
    :param values:  数据
    :param decimals: 保留小数位数
    :return: 转换后的数据
    """
    if values is None:
        return nodata
    datas = np.asarray(values)
    datas[np.isnan(datas)] = nodata
    datas = np.around(datas.tolist(), decimals=decimals)
    return datas.tolist()


def get_ds_coord_name(ds: xr.Dataset):
    """
    获取数据集的坐标信息
    :param ds: 数据集
    :return: tuple
    """
    coords = list(ds.coords)
    if var.LAT in coords and var.LON in coords:
        return var.LAT, var.LON
    elif var.LATITUDE in coords and var.LONGITUDE in coords:
        return var.LATITUDE, var.LONGITUDE
    else:
        raise ValueError("数据集坐标信息异常")


def get_lat_lon_range(ds: xr.Dataset, scale=3):
    """
    获取当前ds中的最大最小经纬度， 以及经纬度个数
    :param ds: ds
    :param scale: 经纬度保留小数位数
    :return: tuple
    """
    lat_key, lon_key = get_ds_coord_name(ds)
    lat = ds[lat_key]
    lon = ds[lon_key]
    min_lat = lat.data.min()
    max_lat = lat.data.max()
    min_lon = lon.data.min()
    max_lon = lon.data.max()
    return (
        round(min_lat, scale), round(max_lat, scale), round(min_lon, scale), round(max_lon, scale), lat.size, lon.size)


def get_ds_lat_lon_step(ds: xr.Dataset, scale=3):
    """
    获取当前ds中的经纬度间隔
    :param ds: ds
    :param scale: 小数位数
    :return: tuple
    """
    lat_key, lon_key = get_ds_coord_name(ds)
    if len(ds[lat_key]) == 0 or len(ds[lon_key]) == 0:
        raise ValueError("数据集坐标数据异常")
    elif len(ds[lat_key]) == 1 and len(ds[lon_key]) == 1:
        lat_step = xr.DataArray(np.array([0]))
        lon_step = xr.DataArray(np.array([0]))
    elif len(ds[lon_key]) == 1:
        lon_step = xr.DataArray(np.array([0]))
        lat_step = abs(ds[lat_key][1] - ds[lat_key][0])
    elif len(ds[lat_key]) == 1:
        lat_step = xr.DataArray(np.array([0]))
        lon_step = abs(ds[lon_key][1] - ds[lon_key][0])
    else:
        lat_step = abs(ds[lat_key][1] - ds[lat_key][0])
        lon_step = abs(ds[lon_key][1] - ds[lon_key][0])
    return round(lat_step.data.tolist(), scale), round(lon_step.data.tolist(), scale)


def get_ds_date_times(ds: xr.Dataset, date_format='%Y-%m-%d %H:%M:%S'):
    """
    获取当前ds的时间lst
    :param ds: ds
    :param date_format: 时间格式
    :return: lst
    """
    coords = list(ds.coords)
    if var.TIME in coords:
        # 这里根据nc文件时间维度存储格式处理
        datetime_index = pd.DatetimeIndex(ds.indexes[var.TIME])
        return datetime_index.strftime(date_format).tolist()
    else:
        raise ValueError("数据集时间key错误！")

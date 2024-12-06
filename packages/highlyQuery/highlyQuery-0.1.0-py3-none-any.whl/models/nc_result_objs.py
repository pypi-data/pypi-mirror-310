"""
nc格点结果对象集对象
@Date    : 2024/11/23
@Author  : YueJiang
@File    : nc_result_objs.py
@Software: PyCharm  
"""
from typing import List


class BaseItemGridObj(object):
    def __init__(self, date_time, grid_data):
        """
        单个格点数据
        :param date_time: 时间
        :param grid_data: 格点数据
        """
        self.date_time = date_time
        self.grid_data = grid_data


class BaseNcResultObj(object):
    def __init__(self, grid_data, date_times=None,
                 lat_step=None, lon_step=None, lat_cnt=None, lon_cnt=None,
                 min_lat=None, max_lat=None, min_lon=None, max_lon=None):
        """
        基础nc文件结果集对象
        :param grid_data:   格点数据
        :param date_times:  时间轴
        :param lat_step: 纬度步长
        :param lon_step: 经度步长
        :param lat_cnt: 纬度个数
        :param lon_cnt: 经度个数
        :param min_lat: 格点最小纬度
        :param max_lat: 格点最大经度
        :param min_lon: 格点最小经度
        :param max_lon: 格点最大经度
        """
        self.lon_cnt = lon_cnt
        self.lat_cnt = lat_cnt
        self.max_lon = max_lon
        self.min_lon = min_lon
        self.max_lat = max_lat
        self.min_lat = min_lat
        self.lon_step = lon_step
        self.lat_step = lat_step
        self.grid_data = grid_data
        self.date_times = date_times

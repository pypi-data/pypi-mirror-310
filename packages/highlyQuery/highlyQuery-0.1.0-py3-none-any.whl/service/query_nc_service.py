"""
查询nc服务
@Date    : 2024/11/22
@Author  : YueJiang
@File    : query_nc_service.py
@Software: PyCharm  
"""
from models.nc_query_objs import BaseNcQueryObj
import utils.nc_query_util as nqu
import consts.common_vars as var
from models.nc_result_objs import BaseNcResultObj


def query_nc_daily(nc_query_obj: BaseNcQueryObj, begin_time=None, end_time=None):
    ds = nc_query_obj.get_sel_time_ds(begin_time, end_time)
    # 经纬度信息
    min_lat, max_lat, min_lon, max_lon, lat_cnt, lon_cnt = nqu.get_lat_lon_range(ds)
    lat_step, lon_step = nqu.get_ds_lat_lon_step(ds)
    # 时间信息
    date_times = nqu.get_ds_date_times(ds)
    # 数据集
    da = nc_query_obj.get_sel_time_da(ds)
    grid_data = nqu.trans_data_nan(da.data)
    return BaseNcResultObj(grid_data=grid_data, date_times=date_times,
                           lat_step=lat_step, lon_step=lon_step, lat_cnt=lat_cnt, lon_cnt=lon_cnt,
                           min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)

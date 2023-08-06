#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/10/28 14:43
@Author   : ji hao ran
@File     : tools.py
@Project  : modelBase
@Software : PyCharm
"""

from .tools import Jet, JetTimeStamp, JetEncoder
from typing import Union, Iterable
import pandas as pd
from pandas import DataFrame
import numpy as np
import simplejson as json
import requests
import sqlalchemy
from kafka import KafkaProducer
from tqdm import tqdm
import warnings
from functools import reduce

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

"""
数据源模块，操作mysql,rtdb实时库，kafka消息队列等不同数据源。
"""
__all__ = ['Mysql', 'Rtdb', 'Kafka']


class Mysql(Jet):
    """
    MySQL数据库操作，读取，写入
    """

    def __init__(self,
                 host: str = '192.168.1.240',
                 port: int = 3306,
                 user: str = 'root',
                 pw: str = 'jizhongjieneng9-28',
                 name: str = 'jet_rtdb_v10_prod_4_hongbo'):
        """

        :param host: 数据库地址
        :param port: 端口
        :param user: 用户名
        :param pw: 密码
        :param name: 数据库名称
        """

        self.host = host
        self.port = port
        self.user = user
        self.pw = pw
        self.name = name

    @property
    def connect(self):
        # 数据库连接
        c = f'mysql+pymysql://{self.user}:{self.pw}@{self.host}:{self.port}/{self.name}?charset=utf8'
        con = sqlalchemy.create_engine(c)
        return con

    def _table_exist(self, table_name: str):
        """判断表格是否存在

        :param table_name: 表格名
        :return: 是否存在
        :rtype: bool
        """
        with self.connect.connect() as con:
            sql = 'show tables;'
            tables = con.execute(sql).fetchall()
            for i in tables:
                if table_name == i[0]:
                    return True
            return False

    def write(self, records: Union[DataFrame, dict], table_name: str, if_exists='append'):
        """
        向mysql数据库写入数据函数,数据库中无表会自动创建

        :param records: 数据
        :param table_name: 表格名字
        :param if_exists: 表格存在插入模式，默认追加，可选[fail,append,replace]
        :return:
        """
        if records is None:
            raise ValueError(f'{self.meta} 数据为空！')
        else:
            try:
                # 转为dataFrame
                record_df = pd.DataFrame(records, index=[0]) if isinstance(records, dict) else records
                # 数据写入表
                # if not record_df.empty:
                record_df.to_sql(table_name, self.connect, if_exists=if_exists, index=False)
            except Exception as e:  # 报错则输出错误
                raise e

    def _read(self, table_name: str):
        """读取一个表格全部内容

        :param table_name: 表格名，表格不存在返回None
        :return: 全部表格内容
        """
        if self._table_exist(table_name):
            return pd.read_sql_table(table_name, self.connect)
        else:
            return None

    def read(self, table_names: Union[str, list]):
        """
        从数据库中获取表的全部数据

        :param table_names: 一个或多个表格名字
        :return: 查询的表格数据
        """
        try:
            if isinstance(table_names, str):
                return self._read(table_names)
            else:
                return list(map(self._read, table_names))
        except Exception as e:  # 报错则输出错误
            raise e

    def delete(self, table_name: str, row_index=None):
        """删除表行，默认清空

        :param table_name: 表名
        :param row_index: 行索引
        """
        df = self.read(table_name)
        if df is not None:  # 表存在
            if row_index is None:  # 清空表格内容
                self.write(pd.DataFrame(columns=df.columns), table_name, 'replace')
            else:
                self.write(df.drop(row_index), table_name, 'replace')

    def update(self, table_name: str, row_index, col_index, value):
        """
        更新表中的记录
        """
        df = self.read(table_name)
        if df is not None:
            df.loc[row_index, col_index] = value
            self.write(df, table_name, 'replace')


class Rtdb(Jet):
    """
    jet RTDB V10实时库数据操作，插入，查询，删除
    """

    def __init__(self, point: Iterable, start_time=None, end_time=None, host: int = 240, **kwargs):
        """

        :param point: RTDB实时库测点
        :param start_time: 开始时间 ,jetTimeStamp输入格式
        :param end_time: 结束时间 ,jetTimeStamp输入格式
        :param host: 实时库地址，默认240，即192.168.1.240，查询临港项目设置为234
        :param kwargs: jetTimeStamp关键字参数
        """
        self.check('len(point)>0', scope=locals())
        # 实时库测点转为list
        self.point = [point] if isinstance(point, str) else point
        self.host = host
        # 开始和结束时间转为毫秒
        self.start_time = JetTimeStamp(start_time, **kwargs).ms
        self.end_time = JetTimeStamp(end_time, **kwargs).ms
        self._headers = {"Content-Type": "application/json"}
        self._insert_url = f'{self.link}/api/v1/insertSampleData'  # 插入数据接口
        self._sample_url = f'{self.link}/api/v1/querySampleData'  # 查询历史数据接口
        self._history_url = f"{self.link}/api/v1/queryHisData"  # 查询历史数据接口(固定时间间隔查询)
        self._latest_url = f"{self.link}/api/v1/queryLastSampleData"  # 查询最新数据接口
        self._delete_url = f"{self.link}/api/v1/deleteSampleData"  # 删除数据接口

    @property
    def link(self):
        return f'http://192.168.1.{self.host}:8055'

    @staticmethod
    def _convert_insert_json(df: DataFrame, cls, split_n: int = 5000):
        """
        数据框转为插入api的json
        :param df: pandas dataframe
        :param cls: json转换的基类
        :param split_n: 列表分组长度，每次插入一组数据
        :return:
        """
        # 构造目标列表
        object_list = []
        # 数据框元素逐个加入
        for i in range(df.shape[0]):
            for j in range(df.shape[1] - 1):
                point = df.columns[j + 1]
                timestamp = df.iloc[i, 0]
                value = df.iloc[i, j + 1]
                if not np.isnan(value):  # value为nan则过滤(接口要求，空值不能插入！)
                    object_list.append({'point': point, 'timestamp': timestamp, 'value': value})
        # 分割长度小于等于列表长度
        split_n = split_n if split_n <= len(object_list) else len(object_list)
        # list 按split_n分组
        object_list_group = [object_list[i:i + split_n] for i in range(0, len(object_list), split_n)]
        # 每组转为json，添加进度条
        js = [json.dumps(i, cls=cls, ignore_nan=True) for i in tqdm(object_list_group, desc='Convert')]
        return js

    def _insert(self, url, js, headers):
        # 请求
        r = requests.post(url, js, headers=headers)
        if r.ok:
            raw_dict = json.loads(r.content)
            if raw_dict.get('opResult') == 'SUCCESS':
                print(self.success)
            else:
                if raw_dict.get('msg') is None:
                    print(f'{self.fail}(empty)')
                else:
                    print(self.fail, raw_dict.get('msg'))
        else:
            print(f'{self.fail} status code {r.status_code}')

    def insert(self, obj: Union[DataFrame, dict]):
        """
        向实时库插入测点数据

        :param obj: pandas dataframe类型:第一列为时间列，列名任意，数值为毫秒时间戳或者pandas Timestamp；
        第二列及以后列名为测点名，数值为测点数值。dict类型,key为point,timestamp,value
        :return:
        """

        if obj is None:
            print(f'{self.fail} (empty)')
        else:
            try:
                if isinstance(obj, dict):
                    body_json = json.dumps([obj], cls=JetEncoder)
                    self._insert(self._insert_url, body_json, self._headers)
                else:
                    body_json_group = self._convert_insert_json(obj, cls=JetEncoder)
                    for i in tqdm(body_json_group, desc='Insert'):
                        self._insert(self._insert_url, i, self._headers)
            except Exception as e:
                raise e

    def _list_parse(self, response_list: list):
        """列表解析

        :param response_list: 响应的列表
        """
        df_list = [self.dict_to_df(i) for i in response_list]
        df = reduce(lambda x, y: pd.merge(x, y, how='outer', on='timestamps'), df_list)
        if not df.empty:
            df.timestamps = df.timestamps.map(lambda x: JetTimeStamp(x).ts)
        df.set_index(keys='timestamps', inplace=True)
        return df

    @staticmethod
    def dict_to_df(x: dict):
        """字典转为数据框

        :param x: 实时库响应数据中的字典
        """
        if x.get('timestamps') is None:
            return pd.DataFrame(columns=['timestamps', x.get('point')])
        else:
            df = pd.DataFrame({k: v for k, v in x.items() if k in ['timestamps', 'values']})
            df.rename(columns={'values': x.get('point')}, inplace=True)
            return df

    def query_sample(self):
        """
        查询实时库历史真实数据
        """
        try:
            # 构造request的body
            body_json = json.dumps({'points': self.point,
                                    'startTime': self.start_time,
                                    'endTime': self.end_time}, cls=JetEncoder)
            r = requests.post(self._sample_url, body_json, headers=self._headers)
            if r.ok:
                raw_list = json.loads(r.content)
                df = self._list_parse(raw_list)
                print(self.success, f'(points:{len(self.point)},point name:{list(self.point)[0]}...)')
                return df
            else:
                raise ValueError(f'{self.fail} status code {r.status_code}')
        except Exception as e:
            print(self.fail)
            raise e

    @staticmethod
    def _history_parse(response_dict: dict):
        """
        解析历史接口响应的数据为数据框
        :param response_dict: 响应的字典数据
        :return:
        """
        # 数据框格式
        df_dict = {k: v for k, v in response_dict.items() if k == 'timestamps'}
        for i in range(response_dict.get("values").__len__()):
            k = response_dict.get("values")[i].get('metricName')
            v = response_dict.get("values")[i].get('values')
            v = v if v else None
            df_dict[k] = v
        if df_dict.get('timestamps') is None:
            df = pd.DataFrame(columns=df_dict.keys())
        else:
            df = pd.DataFrame(df_dict)
            df.timestamps = df.timestamps.map(lambda x: JetTimeStamp(float(x)).ts)
        df.set_index(keys='timestamps', inplace=True)
        return df

    def query_history(self, **kwargs):
        """
        查询实时库历史数据 可以完成多测点相同（或不同）时段的数据查询

        :param kwargs: 查询数据的其他关键字参数,interval,查询间隔，unit,查询单位
        :return: 测点数据
        """
        try:
            # 构造request的body
            interval = kwargs.get('interval', 5)
            unit = kwargs.get('unit', 'minutes')
            body_json = json.dumps({'points': self.point,
                                    'startTime': self.start_time,
                                    'endTime': self.end_time,
                                    "interval": interval,
                                    "unit": unit}, cls=JetEncoder)
            r = requests.post(self._history_url, body_json, headers=self._headers)
            if r.ok:
                raw_dict = json.loads(r.content)
                print(self.success, f'(points:{len(self.point)},point name:{list(self.point)[0]}...)')
            else:
                raise ValueError(f'{self.fail} status code {r.status_code}')
            # 返回结果
            return self._history_parse(raw_dict)
        except Exception as e:
            print(self.fail)
            raise e

    def query_latest(self):
        """
        查询实时库测点最新数据

        :return: 测点数据
        """
        try:
            # 构造request的body
            body_json = json.dumps({'points': self.point}, cls=JetEncoder)
            # 请求
            r = requests.post(self._latest_url, body_json, headers=self._headers)
            if r.ok:
                raw_list = json.loads(r.content)
                print(self.success, f'(points:{len(self.point)},point name:{list(self.point)[0]}...)')
            else:
                raise ValueError(f'{self.fail} status code {r.status_code}')
            # 返回结果
            return self._list_parse(raw_list)
        except Exception as e:
            print(self.fail)
            raise e

    def delete(self):
        """
        删除实时库测点数据

        :return:
        """
        # 构造request的body
        body_json = json.dumps({'points': self.point,
                                'startTime': self.start_time,
                                'endTime': self.end_time}, cls=JetEncoder)
        # 请求
        r = requests.post(self._delete_url, body_json, headers=self._headers)
        raw_dict = json.loads(r.content)
        if raw_dict.get('opResult') == 'SUCCESS':
            print(self.success, f'(points:{len(self.point)},point name:{list(self.point)[0]}...)')
        else:
            raise ValueError(self.fail)


class Kafka:

    def __init__(self, server: str = 'test4.jet:9092', topic: str = 'JET-101-DIAGNOSIS-RESULT-JET'):
        """

        :param server: kafka主机
        :param topic: 消息队列主题
        """
        self.server = server
        self.topic = topic

    @staticmethod
    def _value_serializer(obj):
        """kafka消息序列化器"""
        return json.dumps(obj, cls=JetEncoder).encode('ascii')

    def produce(self, value):
        """生产kafka"""
        try:
            # 生产者
            producer = KafkaProducer(bootstrap_servers=self.server, value_serializer=self._value_serializer)
            # 发送数据
            producer.send(topic=self.topic, value=value)
            # 关闭生产者
            producer.close()
        except Exception as e:
            raise e

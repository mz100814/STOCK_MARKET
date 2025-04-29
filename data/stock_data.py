#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import akshare as ak
import datetime

class StockData:
    """
    股票数据获取与处理类
    
    负责从各种数据源获取股票数据，并进行必要的预处理
    """
    
    def __init__(self, stock_code, start_date, end_date=None):
        """
        初始化股票数据类
        
        参数:
            stock_code (str): 股票代码，如 '000001'
            start_date (str): 开始日期，格式 'YYYY-MM-DD'
            end_date (str): 结束日期，格式 'YYYY-MM-DD'，默认为当前日期
        """
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.datetime.now().strftime('%Y-%m-%d')
        self.data = None
        
    def get_stock_data(self):
        """
        获取股票数据
        
        返回:
            pandas.DataFrame: 包含股票数据的DataFrame
        """
        try:
            # 使用akshare获取A股历史数据
            # 对于上证股票，需要添加前缀"sh"，深证股票需要添加前缀"sz"
            prefix = "sh" if self.stock_code.startswith("6") else "sz"
            stock_code_with_prefix = f"{prefix}{self.stock_code}"
            
            # 使用stock_zh_a_daily API获取数据
            stock_data = ak.stock_zh_a_daily(
                symbol=stock_code_with_prefix,
                start_date=self.start_date.replace('-', ''),
                end_date=self.end_date.replace('-', '')
            )
            
            # akshare返回的列名为英文，需要重命名为中文以保持代码一致性
            stock_data.rename(columns={
                'date': '日期',
                'open': '开盘',
                'high': '最高',
                'low': '最低',
                'close': '收盘',
                'volume': '成交量',
                'amount': '成交额',
                'outstanding_share': '流通股本',
                'turnover': '换手率'
            }, inplace=True)
            
            stock_data['日期'] = pd.to_datetime(stock_data['日期'])
            stock_data.set_index('日期', inplace=True)
            
            # 确保数据按日期排序
            self.data = stock_data.sort_index()
            print(f"成功获取 {self.stock_code} 从 {self.start_date} 到 {self.end_date} 的数据")
            return self.data
            
        except Exception as e:
            print(f"获取数据时出错: {e}")
            return None
    
    def get_data(self):
        """获取当前数据，如果尚未获取则进行获取"""
        if self.data is None:
            return self.get_stock_data()
        return self.data
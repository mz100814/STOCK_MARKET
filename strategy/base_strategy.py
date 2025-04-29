#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """
    交易策略基类
    
    定义了交易策略的通用接口和方法，所有具体策略都应该继承此类
    """
    
    def __init__(self, data=None):
        """
        初始化策略基类
        
        参数:
            data (pandas.DataFrame): 股票数据
        """
        self.data = data
        self.positions = None
        self.capital = 100000  # 初始资金
        self.shares = 0  # 持有股数
        
    def set_data(self, data):
        """设置股票数据"""
        self.data = data
        
    @abstractmethod
    def calculate_indicators(self):
        """
        计算策略所需的技术指标
        
        这是一个抽象方法，需要由子类实现
        """
        pass
        
    @abstractmethod
    def generate_signals(self):
        """
        生成交易信号
        
        这是一个抽象方法，需要由子类实现
        """
        pass
    
    def backtest(self):
        """回测策略"""
        if '信号' not in self.data.columns:
            print("请先生成交易信号")
            return False
            
        # 初始化资金和持仓
        initial_capital = self.capital
        self.data['资金'] = initial_capital
        self.data['持仓'] = 0
        self.data['持仓价值'] = 0
        self.data['总资产'] = initial_capital
        
        current_position = 0  # 当前持仓状态 (0: 空仓, 1: 持仓)
        
        for i in range(1, len(self.data)):
            # 默认保持前一天的状态
            self.data['资金'].iloc[i] = self.data['资金'].iloc[i-1]
            self.data['持仓'].iloc[i] = self.data['持仓'].iloc[i-1]
            
            price = self.data['收盘'].iloc[i]
            
            # 买入信号，并且当前空仓
            if self.data['信号'].iloc[i] == 1 and current_position == 0:
                # 计算可买入的股数（假设可以买入零碎股）
                available_capital = self.data['资金'].iloc[i]
                shares_to_buy = int(available_capital / price)  # 整数股
                
                if shares_to_buy > 0:
                    cost = shares_to_buy * price
                    self.data['资金'].iloc[i] -= cost
                    self.data['持仓'].iloc[i] = shares_to_buy
                    current_position = 1
                    print(f"日期: {self.data.index[i]}, 买入: {shares_to_buy}股, 价格: {price:.2f}")
                
            # 卖出信号，并且当前持仓
            elif self.data['信号'].iloc[i] == -1 and current_position == 1:
                shares_to_sell = self.data['持仓'].iloc[i]
                
                if shares_to_sell > 0:
                    revenue = shares_to_sell * price
                    self.data['资金'].iloc[i] += revenue
                    self.data['持仓'].iloc[i] = 0
                    current_position = 0
                    print(f"日期: {self.data.index[i]}, 卖出: {shares_to_sell}股, 价格: {price:.2f}")
                    
            # 更新持仓价值和总资产
            self.data['持仓价值'].iloc[i] = self.data['持仓'].iloc[i] * price
            self.data['总资产'].iloc[i] = self.data['资金'].iloc[i] + self.data['持仓价值'].iloc[i]
            
        # 计算回测结果
        self.calculate_performance()
        return True
    
    def calculate_performance(self):
        """计算策略表现"""
        # 确保有回测数据
        if '总资产' not in self.data.columns:
            print("请先进行回测")
            return False
            
        # 初始资金
        initial_capital = self.capital
        # 最终资金
        final_capital = self.data['总资产'].iloc[-1]
        # 总收益率
        total_return = (final_capital - initial_capital) / initial_capital * 100
        # 年化收益率 (假设一年有252个交易日)
        days = (self.data.index[-1] - self.data.index[0]).days
        annual_return = (final_capital / initial_capital) ** (365 / days) - 1
        annual_return_pct = annual_return * 100
        
        # 最大回撤
        self.data['累计最大资产'] = self.data['总资产'].cummax()
        self.data['回撤'] = (self.data['总资产'] - self.data['累计最大资产']) / self.data['累计最大资产'] * 100
        max_drawdown = self.data['回撤'].min()
        
        # 输出结果
        print("\n==== 策略表现 ====")
        print(f"初始资金: {initial_capital:.2f}")
        print(f"最终资金: {final_capital:.2f}")
        print(f"总收益率: {total_return:.2f}%")
        print(f"年化收益率: {annual_return_pct:.2f}%")
        print(f"最大回撤: {max_drawdown:.2f}%")
        print(f"交易次数: {len(self.data[self.data['信号'] != 0])}")
        
        return {
            'initial_capital': initial_capital,
            'final_capital': final_capital,
            'total_return': total_return,
            'annual_return': annual_return_pct,
            'max_drawdown': max_drawdown,
            'trade_count': len(self.data[self.data['信号'] != 0])
        }
    
    @abstractmethod
    def plot_results(self):
        """
        绘制回测结果图表
        
        这是一个抽象方法，需要由子类实现
        """
        pass
        
    def run(self, data=None):
        """
        运行完整的策略流程
        
        参数:
            data (pandas.DataFrame): 股票数据，如果不提供则使用已有数据
        """
        if data is not None:
            self.set_data(data)
            
        if self.data is None:
            print("没有数据，无法运行策略")
            return False
            
        if not self.calculate_indicators():
            return False
            
        if not self.generate_signals():
            return False
            
        if not self.backtest():
            return False
            
        if not self.plot_results():
            return False
            
        return True
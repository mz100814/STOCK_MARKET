#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.base_strategy import BaseStrategy

class MACDStrategy(BaseStrategy):
    """
    MACD金叉死叉策略
    
    MACD指标由三部分组成：
    1. DIF (Differential): 快速EMA与慢速EMA的差值
    2. DEA (Signal): DIF的移动平均线
    3. MACD柱: DIF与DEA的差值
    
    金叉: 当DIF从下向上穿越DEA，形成买入信号
    死叉: 当DIF从上向下穿越DEA，形成卖出信号
    """
    
    def __init__(self, data=None, fast_period=12, slow_period=26, signal_period=9):
        """
        初始化MACD策略
        
        参数:
            data (pandas.DataFrame): 股票数据
            fast_period (int): 快速EMA周期，默认为12
            slow_period (int): 慢速EMA周期，默认为26
            signal_period (int): 信号线周期，默认为9
        """
        super().__init__(data)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
            
    def calculate_indicators(self):
        """计算MACD指标"""
        if self.data is None or self.data.empty:
            print("没有数据，请先设置股票数据")
            return False
        
        # 计算EMA
        self.data['EMA_fast'] = self.data['收盘'].ewm(span=self.fast_period, adjust=False).mean()
        self.data['EMA_slow'] = self.data['收盘'].ewm(span=self.slow_period, adjust=False).mean()
        
        # 计算DIF (MACD Line)
        self.data['DIF'] = self.data['EMA_fast'] - self.data['EMA_slow']
        
        # 计算DEA (Signal Line)
        self.data['DEA'] = self.data['DIF'].ewm(span=self.signal_period, adjust=False).mean()
        
        # 计算MACD柱状图
        self.data['MACD'] = (self.data['DIF'] - self.data['DEA']) * 2
        
        print("MACD指标计算完成")
        return True
        
    def generate_signals(self):
        """生成交易信号"""
        if 'DIF' not in self.data.columns or 'DEA' not in self.data.columns:
            print("请先计算MACD指标")
            return False
            
        # 初始化信号列
        self.data['信号'] = 0
        
        # 计算金叉和死叉
        for i in range(1, len(self.data)):
            # 金叉: DIF从下向上穿越DEA
            if (self.data['DIF'].iloc[i-1] < self.data['DEA'].iloc[i-1] and 
                self.data['DIF'].iloc[i] > self.data['DEA'].iloc[i]):
                self.data['信号'].iloc[i] = 1  # 买入信号
                
            # 死叉: DIF从上向下穿越DEA
            elif (self.data['DIF'].iloc[i-1] > self.data['DEA'].iloc[i-1] and 
                  self.data['DIF'].iloc[i] < self.data['DEA'].iloc[i]):
                self.data['信号'].iloc[i] = -1  # 卖出信号
                
        print("交易信号生成完成")
        return True
    
    def plot_results(self):
        """绘制回测结果图表"""
        if '总资产' not in self.data.columns:
            print("请先进行回测")
            return False
            
        plt.figure(figsize=(14, 12))
        
        # 绘制价格和均线
        plt.subplot(3, 1, 1)
        plt.plot(self.data.index, self.data['收盘'], label='收盘价')
        plt.plot(self.data.index, self.data['EMA_fast'], label=f'快速EMA({self.fast_period})')
        plt.plot(self.data.index, self.data['EMA_slow'], label=f'慢速EMA({self.slow_period})')
        
        # 标记买入和卖出点
        buy_signals = self.data[self.data['信号'] == 1]
        sell_signals = self.data[self.data['信号'] == -1]
        
        plt.scatter(buy_signals.index, buy_signals['收盘'], marker='^', color='g', s=100, label='买入信号')
        plt.scatter(sell_signals.index, sell_signals['收盘'], marker='v', color='r', s=100, label='卖出信号')
        
        plt.title('股票价格与交易信号')
        plt.xlabel('日期')
        plt.ylabel('价格')
        plt.legend()
        plt.grid(True)
        
        # 绘制MACD指标
        plt.subplot(3, 1, 2)
        plt.plot(self.data.index, self.data['DIF'], label='DIF')
        plt.plot(self.data.index, self.data['DEA'], label='DEA')
        
        # 绘制MACD柱状图
        plt.bar(self.data.index, self.data['MACD'], color=['g' if x > 0 else 'r' for x in self.data['MACD']], label='MACD柱')
        
        plt.title('MACD指标')
        plt.xlabel('日期')
        plt.ylabel('值')
        plt.legend()
        plt.grid(True)
        
        # 绘制资金曲线
        plt.subplot(3, 1, 3)
        plt.plot(self.data.index, self.data['总资产'], label='总资产')
        plt.plot(self.data.index, self.data['累计最大资产'], linestyle='--', label='历史最高资产')
        
        plt.title('资金曲线')
        plt.xlabel('日期')
        plt.ylabel('资产')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('macd_strategy_result.png')
        plt.show()
        
        return True
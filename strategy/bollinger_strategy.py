#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.base_strategy import BaseStrategy

class BollingerStrategy(BaseStrategy):
    """
    布林带交易策略
    
    布林带指标由三条线组成：
    1. 中轨（Middle Band）：通常是N日移动平均线
    2. 上轨（Upper Band）：中轨 + K倍标准差
    3. 下轨（Lower Band）：中轨 - K倍标准差
    
    基本规则：
    1. 价格上穿上轨，超买信号，卖出
    2. 价格下穿下轨，超卖信号，买入
    """
    
    def __init__(self, data=None, window=20, num_std=2):
        """
        初始化布林带策略
        
        参数:
            data (pandas.DataFrame): 股票数据
            window (int): 移动平均窗口大小，默认为20
            num_std (float): 标准差倍数，默认为2
        """
        super().__init__(data)
        self.window = window
        self.num_std = num_std
    
    def calculate_indicators(self):
        """计算布林带指标"""
        if self.data is None or self.data.empty:
            print("没有数据，请先设置股票数据")
            return False
        
        # 计算移动平均线 (中轨)
        self.data['MA'] = self.data['收盘'].rolling(window=self.window).mean()
        
        # 计算标准差
        self.data['STD'] = self.data['收盘'].rolling(window=self.window).std()
        
        # 计算上轨和下轨
        self.data['上轨'] = self.data['MA'] + (self.data['STD'] * self.num_std)
        self.data['下轨'] = self.data['MA'] - (self.data['STD'] * self.num_std)
        
        # 计算%B指标 (价格在布林带中的相对位置)
        self.data['%B'] = (self.data['收盘'] - self.data['下轨']) / (self.data['上轨'] - self.data['下轨'])
        
        print("布林带指标计算完成")
        return True
    
    def generate_signals(self):
        """生成交易信号"""
        if 'MA' not in self.data.columns or '上轨' not in self.data.columns:
            print("请先计算布林带指标")
            return False
        
        # 初始化信号列
        self.data['信号'] = 0
        
        # 处理NaN值
        # 前window个值会因为移动窗口计算而产生NaN
        self.data = self.data.dropna()
        
        for i in range(1, len(self.data)):
            # 股价从下往上穿过下轨，买入信号
            if (self.data['收盘'].iloc[i-1] <= self.data['下轨'].iloc[i-1] and 
                self.data['收盘'].iloc[i] > self.data['下轨'].iloc[i]):
                self.data['信号'].iloc[i] = 1
            
            # 股价从下往上穿过上轨，卖出信号
            elif (self.data['收盘'].iloc[i-1] <= self.data['上轨'].iloc[i-1] and 
                  self.data['收盘'].iloc[i] > self.data['上轨'].iloc[i]):
                self.data['信号'].iloc[i] = -1
        
        print("交易信号生成完成")
        return True
    
    def plot_results(self):
        """绘制回测结果图表"""
        if '总资产' not in self.data.columns:
            print("请先进行回测")
            return False
        
        plt.figure(figsize=(14, 12))
        
        # 绘制股价和布林带
        plt.subplot(3, 1, 1)
        plt.plot(self.data.index, self.data['收盘'], label='收盘价')
        plt.plot(self.data.index, self.data['MA'], label=f'MA({self.window})')
        plt.plot(self.data.index, self.data['上轨'], label=f'上轨 (+{self.num_std}σ)', linestyle='--')
        plt.plot(self.data.index, self.data['下轨'], label=f'下轨 (-{self.num_std}σ)', linestyle='--')
        
        # 标记买入和卖出点
        buy_signals = self.data[self.data['信号'] == 1]
        sell_signals = self.data[self.data['信号'] == -1]
        
        plt.scatter(buy_signals.index, buy_signals['收盘'], marker='^', color='g', s=100, label='买入信号')
        plt.scatter(sell_signals.index, sell_signals['收盘'], marker='v', color='r', s=100, label='卖出信号')
        
        plt.title('股票价格与布林带')
        plt.xlabel('日期')
        plt.ylabel('价格')
        plt.legend()
        plt.grid(True)
        
        # 绘制%B指标
        plt.subplot(3, 1, 2)
        plt.plot(self.data.index, self.data['%B'], label='%B')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.axhline(y=0.5, color='y', linestyle='--')
        plt.axhline(y=0, color='g', linestyle='--')
        
        plt.title('%B指标 (价格在布林带中的相对位置)')
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
        plt.savefig('bollinger_strategy_result.png')
        plt.show()
        
        return True
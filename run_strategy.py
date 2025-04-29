#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
示例脚本：演示如何使用重构后的策略系统
"""

from data.stock_data import StockData
from strategy.macd_strategy import MACDStrategy
from utils.font_utils import set_matplotlib_chinese_font

def run_macd_strategy():
    """运行MACD策略示例"""
    # 设置中文字体
    set_matplotlib_chinese_font()
    
    # 1. 获取股票数据
    stock_code = "000001"  # 平安银行
    start_date = "2022-01-01"
    end_date = "2022-12-31"
    
    # 创建数据获取对象
    stock_data = StockData(stock_code, start_date, end_date)
    # 获取股票数据
    data = stock_data.get_stock_data()
    
    if data is None:
        print("获取数据失败，无法运行策略")
        return
    
    # 2. 创建MACD策略对象
    macd_strategy = MACDStrategy(
        data=data,
        fast_period=12,
        slow_period=26,
        signal_period=9
    )
    
    # 3. 运行策略
    macd_strategy.run()

def main():
    """主函数"""
    run_macd_strategy()

if __name__ == "__main__":
    main()
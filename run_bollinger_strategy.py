#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
示例脚本：演示如何使用布林带策略
"""

from data.stock_data import StockData
from strategy.bollinger_strategy import BollingerStrategy

def run_bollinger_strategy():
    """运行布林带策略示例"""
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
    
    # 2. 创建布林带策略对象
    bollinger_strategy = BollingerStrategy(
        data=data,
        window=20,
        num_std=2
    )
    
    # 3. 运行策略
    bollinger_strategy.run()

def main():
    """主函数"""
    run_bollinger_strategy()

if __name__ == "__main__":
    main()
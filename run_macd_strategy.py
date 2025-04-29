#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
import sys
import io
from data.stock_data import StockData
from strategy.macd_strategy import MACDStrategy
from utils.font_utils import set_matplotlib_chinese_font

# 忽略所有警告
warnings.filterwarnings("ignore")

def main():
    """
    运行MACD金叉死叉策略示例并只输出最终摘要（没有中间过程）
    """
    # 设置中文字体
    set_matplotlib_chinese_font()
    
    # 设置股票代码和时间范围
    stock_code = "601318"  # 中国平安
    start_date = "2021-01-01"
    end_date = "2022-01-01"
    
    # 临时重定向所有输出
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()  # 捕获所有输出但不显示
    
    try:
        # 获取股票数据
        stock_data = StockData(stock_code, start_date, end_date)
        data = stock_data.get_stock_data()
        
        if data is None:
            sys.stdout = original_stdout  # 恢复输出
            print("获取数据失败，退出程序")
            return
        
        # 创建策略实例
        strategy = MACDStrategy(
            data=data,
            fast_period=12,  # 快速EMA周期
            slow_period=26,  # 慢速EMA周期
            signal_period=9   # 信号线周期
        )
        
        # 执行全过程
        strategy.run()
        
        # 获取性能结果
        performance = strategy.calculate_performance()
        
        # 恢复标准输出
        sys.stdout = original_stdout
        
        # 打印精简摘要
        print("\n==== MACD策略回测摘要 ====")
        print(f"股票: {stock_code} | 周期: {start_date} 至 {end_date}")
        print(f"参数: 快线={strategy.fast_period}, 慢线={strategy.slow_period}, 信号线={strategy.signal_period}")
        print("-" * 40)
        print(f"收益分析:")
        print(f"初始资金: {performance['initial_capital']:.2f} 元")
        print(f"最终资金: {performance['final_capital']:.2f} 元")
        print(f"净收益: {performance['final_capital'] - performance['initial_capital']:.2f} 元")
        print(f"总收益率: {performance['total_return']:.2f}%")
        print(f"年化收益率: {performance['annual_return']:.2f}%")
        print(f"最大回撤: {performance['max_drawdown']:.2f}%")
        
        # 获取交易统计
        signals = strategy.data[strategy.data['信号'] != 0]
        buy_count = len(signals[signals['信号'] == 1])
        sell_count = len(signals[signals['信号'] == -1])
        
        # 计算胜率
        profitable_trades = 0
        trade_records = []
        
        # 按日期排序信号
        sorted_signals = signals.sort_index()
        
        # 配对买卖交易
        i = 0
        while i < len(sorted_signals) - 1:
            if sorted_signals.iloc[i]['信号'] == 1 and sorted_signals.iloc[i+1]['信号'] == -1:
                buy_date = sorted_signals.index[i]
                buy_price = sorted_signals.iloc[i]['收盘']
                sell_date = sorted_signals.index[i+1]
                sell_price = sorted_signals.iloc[i+1]['收盘']
                profit = (sell_price - buy_price) / buy_price * 100
                
                # 记录交易对
                trade_records.append({
                    'buy_date': buy_date.strftime('%Y-%m-%d'),
                    'buy_price': buy_price,
                    'sell_date': sell_date.strftime('%Y-%m-%d'),
                    'sell_price': sell_price,
                    'profit_pct': profit
                })
                
                if sell_price > buy_price:
                    profitable_trades += 1
                    
                i += 2
            else:
                i += 1
        
        # 避免除以零
        win_rate = profitable_trades / max(1, len(trade_records)) * 100
        
        print("-" * 40)
        print(f"交易统计:")
        print(f"总信号数: {len(signals)} (买入: {buy_count}, 卖出: {sell_count})")
        print(f"完整交易对: {len(trade_records)}")
        print(f"盈利交易: {profitable_trades}")
        print(f"亏损交易: {len(trade_records) - profitable_trades}")
        print(f"胜率: {win_rate:.2f}%")
    
    except Exception as e:
        # 恢复标准输出
        sys.stdout = original_stdout
        print(f"执行过程中出现错误: {e}")
    
if __name__ == "__main__":
    main()
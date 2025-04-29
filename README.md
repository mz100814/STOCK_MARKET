# 股票量化交易系统

这是一个简单的股票量化交易系统，包含数据获取和不同交易策略的实现。

## 项目结构

```
stock_market/
├── data/                  # 数据模块
│   ├── __init__.py
│   └── stock_data.py      # 股票数据获取类
├── strategy/              # 策略模块
│   ├── __init__.py
│   ├── base_strategy.py   # 基础策略类
│   ├── macd_strategy.py   # MACD策略实现
│   └── bollinger_strategy.py  # 布林带策略实现
├── run_strategy.py    # 运行示例
├── run_bollinger_strategy.py   # 布林带策略运行示例
├── run_macd_strategy.py   # MACD策略运行示例
└── requirements.txt       # 项目依赖
```

## 系统设计

系统采用模块化设计，将数据获取和策略实现分离：

1. **数据模块**：负责从各种数据源获取股票数据并进行预处理
2. **策略模块**：基于获取的数据实现各种交易策略
3. **基础策略类**：定义了通用的回测逻辑，可以被具体策略继承

## 已实现的策略

1. **MACD策略**：基于MACD金叉、死叉信号进行交易
2. **布林带策略**：基于价格突破布林带上下轨产生交易信号

## 使用方法

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行MACD策略示例

```bash
python run_strategy_example.py
```

### 运行布林带策略示例

```bash
python run_bollinger_example.py
```

## 添加新策略

要添加新的交易策略，只需继承`BaseStrategy`类并实现以下方法：

1. `calculate_indicators`: 计算策略所需的技术指标
2. `generate_signals`: 根据指标生成交易信号
3. `plot_results`: 绘制回测结果图表

## 依赖

- Python 3.6+
- pandas
- numpy
- matplotlib
- akshare
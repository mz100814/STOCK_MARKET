#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
字体工具模块，用于解决matplotlib中文显示问题
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os

def set_matplotlib_chinese_font():
    """
    设置matplotlib支持中文显示
    
    根据不同操作系统设置合适的中文字体
    """
    # 检测操作系统
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        # macOS中常见的中文字体路径
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',  # 苹方字体
            '/System/Library/Fonts/STHeiti Light.ttc',  # 黑体-简 细体
            '/System/Library/Fonts/STHeiti Medium.ttc',  # 黑体-简 中黑
            '/Library/Fonts/Songti.ttc'  # 宋体
        ]
        
        # 尝试设置字体
        for path in font_paths:
            if os.path.exists(path):
                prop = fm.FontProperties(fname=path)
                plt.rcParams['font.family'] = prop.get_name()
                break
                
        # 如果找不到具体字体文件，尝试使用字体名称
        if 'font.family' not in plt.rcParams or plt.rcParams['font.family'] == 'sans-serif':
            plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STHeiti', 'Heiti TC', 'Microsoft YaHei'] + plt.rcParams['font.sans-serif']
    
    elif system == 'Windows':
        # Windows中文字体
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'NSimSun'] + plt.rcParams['font.sans-serif']
    
    else:  # Linux
        # Linux中文字体
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'SimHei'] + plt.rcParams['font.sans-serif']
    
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False
    
    return True
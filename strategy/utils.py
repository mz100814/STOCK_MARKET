#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
工具函数模块，包含各种辅助功能
"""

import matplotlib.pyplot as plt
import matplotlib
import platform
import os

def set_chinese_font():
    """
    设置matplotlib支持中文显示
    """
    # 检测操作系统
    system = platform.system()
    
    if system == 'Windows':
        # Windows系统使用微软雅黑
        font_path = 'C:/Windows/Fonts/msyh.ttc'
        if os.path.exists(font_path):
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        else:
            plt.rcParams['font.sans-serif'] = ['SimHei']
    elif system == 'Darwin':  # macOS
        # macOS系统使用苹方字体或其他常见中文字体
        font_options = ['PingFang SC', 'STHeiti', 'Heiti TC', 'Apple LiGothic Medium']
        
        for font in font_options:
            try:
                matplotlib.font_manager.fontManager.addfont(
                    matplotlib.font_manager.findfont(font))
                plt.rcParams['font.sans-serif'] = [font] + plt.rcParams['font.sans-serif']
                break
            except:
                continue
    else:  # Linux等其他系统
        # Linux系统常见中文字体
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'AR PL UMing CN']
    
    # 用来正常显示负号
    plt.rcParams['axes.unicode_minus'] = False
    
    return True
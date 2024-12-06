# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'Helper'
'''
  * @File    :   Helper.py
  * @Time    :   2024/11/24 19:47:56
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
'''
from shutil import get_terminal_size

terminal_size = get_terminal_size(fallback=(120, 50))


class Helper:
    @staticmethod
    def help_text():
        return f"""
1. fetch_repos  获取所有仓库信息
2. clone_repos  克隆所有仓库, 本地对应目录结构和仓库url相同
"""

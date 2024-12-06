# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "SettingsDelegate"
"""
  * @File    :   SettingsDelegate.py
  * @Time    :   2023/04/23 18:04:42
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""

from pathlib import Path
from abc import ABCMeta, abstractclassmethod


class SettingsDelegate(ABCMeta):
    @abstractclassmethod
    def fetch_settings_cfg_file_path(self) -> Path | None:
        return None

    @abstractclassmethod
    def load_finish(self):
        pass

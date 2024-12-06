# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'Settings'
'''
  * @File    :   Settings.py
  * @Time    :   2024/11/24 20:57:20
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
'''

from pathlib import Path

from xy_settings.Settings import Settings as xy_s

from .GitConfig import GitConfig


class Settings(xy_s):
    default_cfg_path: Path = Path.home().joinpath(".xy_config/xy_git.toml")
    git_config: GitConfig | None = GitConfig()

    def check_cfg_path(self) -> bool:
        return (
            isinstance(self.default_cfg_path, Path)
            and self.default_cfg_path.exists() == True
        )

    def reload(self, settings_cfg_path: Path):
        super().reload(settings_cfg_path)
        self.git_config = self.make_section(GitConfig)

# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'xy_git_config'
'''
  * @File    :   xy_git_config.py
  * @Time    :   2024/11/25 06:49:38
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
'''

from xy_settings.Section.Section import Section


class GitConfig(Section):

    platform: str | int | None
    access_token: str | None

    username: str | None

    def get_name(self) -> str | None:
        return "git_config"

    def _load(self):
        ##################### sync_data ################
        self.platform = self._sync_data("platform", default=0)  # type: ignore
        self.access_token = self._sync_data("access_token", default=None)
        self.username = self._sync_data("username", default=None)
        super()._load()

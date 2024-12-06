# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'Git'
'''
  * @File    :   Git.py
  * @Time    :   2024/11/24 12:15:16
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
'''
import json
import os
from pathlib import Path

from xy_console.utils import print_exe, print_e

from .platform.Platform import EPlatformChannel
from .platform.Platform import Platform
from .platform.Settings import Settings


class Git:

    platform: Platform = Platform()
    settings: Settings = Settings()

    def __init__(self, cfg_path: str | None = None):
        if isinstance(cfg_path, str) and len(cfg_path) > 0:
            self.settings.default_cfg_path = Path(cfg_path)
        if not cfg_path:
            cfg_path = self.settings.default_cfg_path
        if self.settings.check_cfg_path() == True:
            self.settings.load(cfg_path)
            self.platform = Platform(self.settings.git_config.platform)

    def check_channel(
        self,
        platform_code: str | int | None = None,
    ):
        if platform_code is not None:
            self.platform = Platform(platform_code)
        else:
            if (
                self.settings.check_cfg_path() == True
                and self.settings.git_config.platform != None
            ):
                self.platform = Platform(self.settings.git_config.platform)
            else:
                self.platform = Platform(0)

    def get(
        self,
        access_token: str | None = None,
        platform_code: str | int | None = None,
        url: str = "",
        page: int = 1,
        per_page: int = 100,
        type_str: str = "all",
        params: dict = {},
    ):
        self.check_channel(
            platform_code=platform_code,
        )
        if not self.settings.git_config.access_token and not access_token:
            print_e("access_token 未设置和未传入")
            return
        response = self.platform.get(
            url,
            (
                access_token
                if access_token is not None
                else self.settings.git_config.access_token
            ),
            page,
            per_page,
            type_str,
            params,
        )
        print(json.dumps(response))

    def fetch_repos(
        self,
        access_token: str | None = None,
        platform_code: str | int | None = None,
        url: str = "",
        page: int = 1,
        per_page: int = 100,
        type_str: str = "all",
        params: dict = {},
        username: str = "",
    ):
        self.check_channel(
            platform_code=platform_code,
        )
        if not self.settings.git_config.access_token and not access_token:
            print_e("access_token 未设置和未传入")
            return
        if not username:
            username = self.settings.git_config.username
        repos = self.platform.repos(
            url,
            (
                access_token
                if access_token is not None
                else self.settings.git_config.access_token
            ),
            page,
            per_page,
            type_str,
            params,
            username,
        )
        print(json.dumps(repos))

    def clone_repos(
        self,
        access_token: str,
        platform_code: str | int | None = None,
        url: str = "",
        page: int = 1,
        per_page: int = 100,
        type_str: str = "all",
        params: dict = {},
        username: str = "",
    ):
        self.check_channel(
            platform_code=platform_code,
        )
        if not self.settings.git_config.access_token and not access_token:
            print_e("access_token 未设置和未传入")
            return
        if not username:
            username = self.settings.git_config.username
        repos = self.platform.repos(
            url,
            (
                access_token
                if access_token is not None
                else self.settings.git_config.access_token
            ),
            page,
            per_page,
            type_str,
            params,
            username,
        )
        if isinstance(repos, list) and len(repos) > 0:
            for repo in repos:
                if isinstance(repo, dict):
                    self._clone_repos(repo)
        else:
            print_exe("没有找到仓库 或者 api接口版本已更新造成数据不匹配")

    def _clone_repos(self, repo: dict):
        full_name = None
        repo_git_url = None
        match self.platform.channel:
            case EPlatformChannel.GitCode:
                full_name = repo.get("full_name")
                repo_git_url = repo.get("http_url_to_repo")
            case EPlatformChannel.Gitee:
                full_name = repo.get("full_name")
                repo_git_url = repo.get("html_url")
            case EPlatformChannel.GitHub:
                full_name = repo.get("full_name")
                repo_git_url = repo.get("clone_url")
            case _:
                full_name = repo.get("path_with_namespace")
                repo_git_url = repo.get("http_url_to_repo")

        full_path = Path(full_name)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        os.system(f"git clone {repo_git_url} {full_name}")

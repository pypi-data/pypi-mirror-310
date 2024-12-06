# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'platform'
'''
  * @File    :   platform.py
  * @Time    :   2024/11/24 18:27:17
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
'''

from enum import IntEnum

from .gitcode.GitCode import GitCode
from .gitee.Gitee import Gitee
from .github.GitHub import GitHub
from .gitlab.GitLab import GitLab


class EPlatformChannel(IntEnum):

    GitCode = 0
    Gitee = 1
    GitHub = 2
    GitLab = 3

    @staticmethod
    def parse(channel_code: str | int):
        channel_code_lower = (
            channel_code.lower() if isinstance(channel_code, str) else channel_code
        )
        if (
            channel_code_lower == EPlatformChannel.GitCode.name.lower()
            or channel_code_lower == str(EPlatformChannel.GitCode.value)
            or channel_code_lower == EPlatformChannel.GitCode.value
        ):
            return EPlatformChannel.GitCode
        elif (
            channel_code_lower == EPlatformChannel.Gitee.name.lower()
            or channel_code_lower == str(EPlatformChannel.Gitee.value)
            or channel_code_lower == EPlatformChannel.Gitee.value
        ):
            return EPlatformChannel.Gitee
        elif (
            channel_code_lower == EPlatformChannel.GitHub.name.lower()
            or channel_code_lower == str(EPlatformChannel.GitHub.value)
            or channel_code_lower == EPlatformChannel.GitHub.value
        ):
            return EPlatformChannel.GitHub
        else:
            return EPlatformChannel.GitLab


class Platform:
    channel: EPlatformChannel = EPlatformChannel.GitCode

    def __init__(
        self,
        channel_code: str | int = 0,
    ):
        self.channel = EPlatformChannel.parse(channel_code)

    def repos(
        self,
        url: str,
        access_token: str,
        page: int = 1,
        per_page: int = 100,
        type_str: str = "all",
        params: dict = {},
        username: str = "",
    ):
        match self.channel:
            case EPlatformChannel.GitCode:
                return GitCode.repos(
                    access_token,
                    page,
                    per_page,
                )
            case EPlatformChannel.Gitee:
                return Gitee.repos(
                    access_token,
                    page,
                    per_page,
                )
            case EPlatformChannel.GitHub:
                return GitHub.repos(
                    access_token,
                    username,
                    page,
                    per_page,
                    type_str,
                )
            case EPlatformChannel.GitLab:
                return GitLab.repos(
                    access_token,
                    page,
                    per_page,
                )
            case _:
                if isinstance(url, str) and url:
                    return GitLab.get(
                        url,
                        access_token,
                        page,
                        per_page,
                        type_str=type_str,
                        params=params,
                    )
                return None

    def get(
        self,
        url: str,
        access_token: str,
        page: int = 1,
        per_page: int = 100,
        type_str: str = "all",
        params: dict = {},
    ):
        if isinstance(url, str) and url:
            return GitLab.get(
                url,
                access_token,
                page,
                per_page,
                type_str=type_str,
                params=params,
            )
        return None

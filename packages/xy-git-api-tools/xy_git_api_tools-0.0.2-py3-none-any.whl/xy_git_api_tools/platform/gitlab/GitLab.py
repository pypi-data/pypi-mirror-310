# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "GitLab"
"""
  * @File    :   GitLab.py
  * @Time    :   2024/11/24 11:19:01
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""
import requests

from xy_string.utils import is_empty_string

from .urls import api_url


class GitLab:

    @staticmethod
    def get(
        url: str,
        access_token: str,
        page: int = 1,
        per_page: int = 100,
        type_str: str = "",
        params: dict | None = None,
    ):
        query = {
            "private_token": access_token,
            "page": page,
            "per_page": per_page,
            "type": type_str,
        }
        if isinstance(params, dict):
            query.update(params)
        if is_empty_string(url) == False:
            response = requests.get(
                url,
                params=query,
                timeout=30,
            )
            if response and response.status_code == 200:
                return response.json()
        return None

    @staticmethod
    def repos(
        access_token: str,
        page: int = 1,
        per_page: int = 100,
    ) -> list | dict | None:
        url = api_url.get("repos")
        params = {
            "membership": True,
        }
        return GitLab.get(
            url,  # type: ignore
            access_token,
            page,
            per_page,
            params=params,
        )

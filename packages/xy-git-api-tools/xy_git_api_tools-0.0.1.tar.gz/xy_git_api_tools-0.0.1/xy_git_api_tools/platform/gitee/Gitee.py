# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Gitee"
"""
  * @File    :   Gitee.py
  * @Time    :   2024/11/24 10:45:56
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""
import requests

from xy_string.utils import is_empty_string

from .urls import api_url


class Gitee:

    @staticmethod
    def get(
        url: str,
        access_token: str,
        page: int = 1,
        per_page: int = 100,
        params: dict | None = None,
    ):
        query = {
            "access_token": access_token,
            "page": page,
            "per_page": per_page,
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
    ):
        url = api_url.get("repos")
        if is_empty_string(url) == True:
            return None
        return Gitee.get(
            url,  # type: ignore
            access_token,
            page,
            per_page,
        )

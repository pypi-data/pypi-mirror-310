# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "GitHub"
"""
  * @File    :   GitHub.py
  * @Time    :   2024/11/24 10:46:00
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""
import requests
from pathlib import Path

from xy_console.utils import print_e
from xy_string.utils import is_empty_string

from .urls import base_url, api_url


class GitHub:

    @staticmethod
    def get(
        url: str,
        page: int = 1,
        per_page: int = 100,
        params: dict | None = None,
        headers: dict | None = None,
    ):
        query = {
            "page": page,
            "per_page": per_page,
        }
        if isinstance(params, dict):
            query.update(params)
        if is_empty_string(url) == False:
            response = requests.get(
                url,
                params=query,
                headers=headers,
                timeout=30,
            )
            if response and response.status_code == 200:
                return response.json()
        return None

    @staticmethod
    def repos(
        access_token: str,
        username: str,
        page: int = 1,
        per_page: int = 100,
        type_str: str = "all",
    ):
        if not access_token or not username:
            print_e("access_token和username未传入!!!")
            return
        user_repos_url = api_url.get("user_repos")(username)  # type: ignore
        params = {
            "type": type_str,
        }
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {access_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if is_empty_string(username) == True:
            return None
        repos = GitHub.get(
            user_repos_url,  # type: ignore
            page,
            per_page,
            params=params,
            headers=headers,
        )
        if not isinstance(repos, list):
            repos = []
        user_orgs_url = api_url.get("user_orgs")
        org_user_repos_url = api_url.get("org_user_repos")
        organizations = GitHub.get(
            user_orgs_url,
            headers=headers,
        )
        if isinstance(organizations, list):
            for organization in organizations:
                if isinstance(organization, dict):
                    organization_url = organization.get("organization_url")
                    if isinstance(
                        organization_url, str
                    ) and organization_url.startswith(base_url):
                        org_name = Path(organization_url).name
                        org_repos_url = org_user_repos_url(org_name)
                        org_repos = GitHub.get(
                            org_repos_url,
                            headers=headers,
                        )
                        repos.extend(org_repos)
        return repos

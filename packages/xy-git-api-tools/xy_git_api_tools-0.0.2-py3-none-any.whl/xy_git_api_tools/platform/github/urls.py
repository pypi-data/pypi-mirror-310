# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'urls'
'''
  * @File    :   urls.py
  * @Time    :   2024/11/24 12:13:43
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
'''

base_url = "https://api.github.com"

api_url = {
    "user_repos": lambda username: f"{base_url}/users/{username}/repos",
    "user_orgs": f"{base_url}/user/memberships/orgs",
    "org_user_repos": lambda org_name: f"{base_url}/orgs/{org_name}/repos",
}

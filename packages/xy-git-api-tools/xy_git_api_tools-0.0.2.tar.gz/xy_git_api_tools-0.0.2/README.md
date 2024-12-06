# git_api_tools

| [简体中文](./README.md)         | [繁體中文](readme/README.zh-hant.md)        |                      [English](readme/README.en.md)          |
| ----------- | -------------|---------------------------------------|

## 说明

希洋开源软件包运行环境.

## 源码仓库

| [Github](https://github.com/xy-cross-tools/xy_git_api_tools.git)         | [Gitee](https://gitee.com/xy-opensource/xy_git_api_tools.git)        |                      [GitCode](https://gitcode.com/xy-opensource/xy_git_api_tools.git)          |
| ----------- | -------------|---------------------------------------|


## 安装

```bash
# bash
pip install xy_git_api_tools
```

## 使用

> !!! 注意: 当请求GitHub仓库时候必须带上username参数,无论是命令行传入还是配置到配置文件中
> !!! 默认配置文件路径为 ~/.xy_config/xy_git.toml

###### 1. 配置文件

```toml
# config.toml
[git_config]
platform = "github"
# platform = "https://gitlab.com/api/v4/projects"
# platform = 0
# platform = "GitCode"
# platform = "giTcOde"
# platform = "giTCODe"

access_token = "ghp_454545454sadf1dfsa"
# access_token = "glpat-asdjklfjweroijweoirjwoer"

username = "yuyangit"
```

2. 查看命令
```bash
xy_git_api_tools -w list_api
# =========================================================

# 1. fetch_repos  获取所有仓库信息
# 2. clone_repos  克隆所有仓库, 
# 本地对应目录结构和仓库url相同

```

3. 获取所有仓库信息

```bash
xy_git_api_tools -c fetch_repos -cfg ./config.toml
# [
#     {
#         "id": 4357570,
#         "full_name": "xy-opensource/xy_git_api_tools",
#         "human_name": "xy-opensource / xy_git_api_tools",
#         "url": "https://api.gitcode.com/api/v5/repos/xy-opensource/xy_git_api_tools",
#         "namespace": {
#             "id": 3536801,
#             "type": "enterprise",
#             "name": "xy-opensource",
#             "path": "xy-opensource",
#             "html_url": "https://gitcode.com/xy-opensource"
#         },
#         "path": "xy_git_api_tools",
#         "name": "xy_git_api_tools",
#         "description": "\u5173\u4e8eGit\u7684Api\u5de5\u5177",
#         "status": "\u5f00\u59cb",
#         "ssh_url_to_repo": "git@gitcode.com:xy-opensource/xy_git_api_tools.git",
#         "http_url_to_repo": "https://gitcode.com/xy-opensource/xy_git_api_tools.git",
#         "web_url": "https://gitcode.com/xy-opensource/xy_git_api_tools",
#         "created_at": "2024-11-24T13:11:49.606+08:00",
#         "updated_at": "2024-11-24T13:11:49.606+08:00",
#         "homepage": "https://gitcode.com/xy-opensource/xy_git_api_tools",
#         "members": [
#             "yuyangit"
#         ],
#         "assignee": [
#             {
#                 "id": "2173437",
#                 "login": "yuyangit",
#                 "name": "yuyangit",
#                 "avatar_url": "https://cdn-img.gitcode.com/fe/fd/f06483269e5f85434d8dc1aa80c1361e9f1fed704b5681043bed4eecaaffce8e.jpeg?time=1731978609795",
#                 "html_url": "https://gitcode.com/yuyangit",
#                 "type": "User"
#             }
#         ],
#         "forks_count": 0,
#         "stargazers_count": 0,
#         "project_labels": [],
#         "relation": "master",
#         "permission": {
#             "pull": true,
#             "push": true,
#             "admin": true
#         },
#         "internal": false,
#         "open_issues_count": 0,
#         "has_issue": false,
#         "watched": false,
#         "watchers_count": 0,
#         "assignees_number": 1,
#         "enterprise": {
#             "id": 3536801,
#             "path": "xy-opensource",
#             "html_url": "https://gitcode.com/xy-opensource",
#             "type": "enterprise"
#         },
#         "default_branch": "main",
#         "fork": false,
#         "owner": {
#             "id": "2173437",
#             "login": "yuyangit",
#             "name": "yuyangit",
#             "type": "User"
#         },
#         "assigner": {
#             "id": "2173437",
#             "login": "yuyangit",
#             "name": "yuyangit",
#             "type": "User"
#         },
#         "issue_template_source": "project",
#         "language": "Python",
#         "private": false,
#         "public": true
#     },
#     {
#         "id": 4357105,
#         "full_name": "xy-opensource/xy_pypi_builder_mirror",
#         "human_name": "xy-opensource / xy_pypi_builder_mirror",
#         "url": "https://api.gitcode.com/api/v5/repos/xy-opensource/xy_pypi_builder_mirror",
#         "namespace": {
#             "id": 3536801,
#             "type": "enterprise",
#             "name": "xy-opensource",
#             "path": "xy-opensource",
#             "html_url": "https://gitcode.com/xy-opensource"
#         },
#         "path": "xy_pypi_builder_mirror",
#         "name": "xy_pypi_builder_mirror",
#         "description": "\u7f16\u8bd1python\u6a21\u5757\u7684pypi\u73af\u5883\u7684\u955c\u50cf.",
#         "status": "\u5f00\u59cb",
#         "ssh_url_to_repo": "git@gitcode.com:xy-opensource/xy_pypi_builder_mirror.git",
#         "http_url_to_repo": "https://gitcode.com/xy-opensource/xy_pypi_builder_mirror.git",
#         "web_url": "https://gitcode.com/xy-opensource/xy_pypi_builder_mirror",
#         "created_at": "2024-11-24T08:55:04.966+08:00",
#         "updated_at": "2024-11-24T13:05:59.513+08:00",
#         "homepage": "https://gitcode.com/xy-opensource/xy_pypi_builder_mirror",
#         "members": [
#             "yuyangit"
#         ],
#         "assignee": [
#             {
#                 "id": "2173437",
#                 "login": "yuyangit",
#                 "name": "yuyangit",
#                 "avatar_url": "https://cdn-img.gitcode.com/fe/fd/f06483269e5f85434d8dc1aa80c1361e9f1fed704b5681043bed4eecaaffce8e.jpeg?time=1731978609795",
#                 "html_url": "https://gitcode.com/yuyangit",
#                 "type": "User"
#             }
#         ],
#         "forks_count": 0,
#         "stargazers_count": 0,
#         "project_labels": [],
#         "relation": "master",
#         "permission": {
#             "pull": true,
#             "push": true,
#             "admin": true
#         },
#         "internal": false,
#         "open_issues_count": 0,
#         "has_issue": false,
#         "watched": false,
#         "watchers_count": 0,
#         "assignees_number": 1,
#         "enterprise": {
#             "id": 3536801,
#             "path": "xy-opensource",
#             "html_url": "https://gitcode.com/xy-opensource",
#             "type": "enterprise"
#         },
#         "default_branch": "main",
#         "fork": false,
#         "owner": {
#             "id": "2173437",
#             "login": "yuyangit",
#             "name": "yuyangit",
#             "type": "User"
#         },
#         "assigner": {
#             "id": "2173437",
#             "login": "yuyangit",
#             "name": "yuyangit",
#             "type": "User"
#         },
#         "issue_template_source": "project",
#         "language": "Dockerfile",
#         "private": false,
#         "public": true
#     },
# ]
```

3. git clone 所有仓库到本地, 根据仓库地址结构对应路径进行存储

```bash
xy_git_api_tools -c clone_repos -cfg ./config.toml
```

## 许可证
xy_git_api_tools 根据 <木兰宽松许可证, 第2版> 获得许可。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 捐赠
如果小伙伴们觉得这些工具还不错的话，能否请咱喝一杯咖啡呢?  

![pay-total](./readme/pay-total.png)


## 联系方式

```
微信: yuyangiit
邮箱: yuyangit.0515@qq.com
```
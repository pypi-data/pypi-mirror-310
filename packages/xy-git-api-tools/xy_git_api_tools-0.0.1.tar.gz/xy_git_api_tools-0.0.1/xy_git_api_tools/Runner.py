# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'Runner'
'''
  * @File    :   Runner.py
  * @Time    :   2023/06/03 10:29:52
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
'''
from argparse import Namespace
import json

from xy_console.utils import print_exe, print_e
from xy_argparse.ArgParse import ArgParse


import xy_git_api_tools

from .ModuleData import ModuleData
from .Resource import Resource

from .Helper import Helper
from .Git import Git


class Runner(ArgParse):
    _module_data = ModuleData()
    _resource = Resource()

    def __init__(self) -> None:
        self.quick_default_info(xy_git_api_tools.__name__)
        self.description = "Git仓库api工具"

    def main(self):
        self.default_parser()
        self.add_arguments()
        self.run_arguments()

    def add_arguments(self):
        self.add_argument(
            flag="-w",
            name="--work",
            help_text="""
                1. list_api 展示api命令
            """,
        )
        self.add_argument(
            flag="-c",
            name="--command",
            help_text="""
                工作方式: 1. xy_git_api_tools -c <api命令> 根据展示api命令对api进行操作
            """,
        )
        self.add_argument(
            flag="-plt",
            name="--platform",
            help_text="""
                默认: 0, 可选: 0/gitcode, 1/gitee, 2/github, 3/gitlab, 其他对应Gitlab-api的url, 可输入url, 默认https://gitlab.com
            """,
        )
        self.add_argument(
            flag="-cfg",
            name="--config",
            help_text="""
                配置文件路径, 必须是toml格式
                默认: ~/.xy_config/xy_git.toml
            """,
        )
        self.add_argument(
            flag="-at",
            name="--access_token",
            help_text="""
                输入access_token
            """,
        )
        self.add_argument(
            flag="-t",
            name="--type_value",
            help_text="""
                接口type参数
            """,
        )
        self.add_argument(
            flag="-pr",
            name="--params",
            help_text="接口参数字典",
        )
        self.add_argument(
            flag="-p",
            name="--page",
            help_text="接口参数: 页码 => 默认: 1",
        )
        self.add_argument(
            flag="-pp",
            name="--per_page",
            help_text="接口参数: 每页个数 => 默认: 100, 最大100, 最小10",
        )
        self.add_argument(
            flag="-u",
            name="--username",
            help_text="-plt/--platform 为github时候必须传入 GitHub用户名",
        )

    def work(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.work
        return None

    def command(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.command
        return None

    def config(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.config
        return None

    def platform(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.platform
        return None

    def access_token(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.access_token
        return None

    def type_value(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.type_value
        return None

    def params(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.params
        return None

    def page(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.page
        return None

    def per_page(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.per_page
        return None

    def username(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.username
        return None

    def on_arguments(
        self,
        name,
        value,
        arguments=None,
    ):
        if name == "work":
            if value == "list_api":
                self.list_api()
                return False
        elif name == "command":
            self.api_command()
            return False
        return True

    def api_url(self, platform: str | int):
        if isinstance(platform, str) and len(platform) > 0:
            return (
                platform
                if len(platform) >= 10
                and (platform.startswith("http://") or platform.startswith("https://"))
                else ""
            )
        return None

    def api_command(self):
        command = self.command()
        config = self.config()
        platform = self.platform()
        api_url = self.api_url(platform)
        access_token = self.access_token()
        type_value = self.type_value()
        params_text = self.params()
        page = self.page()
        per_page = self.per_page()
        username = self.username()

        if not command:
            print_e(
                "请传入根据 xy_git_api_tools -w list_api 中展示的 -c/--command 参数!!!"
            )
            return
        params = {}
        try:
            params = json.loads(params_text)  # type: ignore
        except:
            params = {}
        try:
            if (
                api_url
                and isinstance(api_url, str)
                and len(api_url) > 0
                and (api_url.startswith("http://") or api_url.startswith("https://"))
            ):
                command = "get"
                platform = "gitlab"
            function = getattr(Git(config), command)  # type: ignore
            function(
                access_token=access_token,
                platform_code=platform,
                url=api_url,
                page=page,
                per_page=per_page,
                type_str=type_value,
                params=params,
                username=username,
            )
        except Exception as e:
            print_e(f"报告错误\n{e.args}")

    def list_api(self):
        print_exe(Helper().help_text())

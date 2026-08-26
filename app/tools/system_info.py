#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：system_info.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 18:35 
@Description： 
'''
from app.tools.base import BaseTool


class SystemInfoTool(BaseTool):

    name = "system_info"

    description = """
    获取当前系统信息，
    包括CPU、内存、磁盘。
    """

    parameters = {}

    async def execute(self, **kwargs):

        return {
            "cpu": "Apple Silicon",
            "memory": "16GB",
            "disk": "SSD"
        }
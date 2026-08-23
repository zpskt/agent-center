#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：registry.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 18:35 
@Description： 
'''
from app.tools.system_info import SystemInfoTool


TOOLS = {
    "system_info": SystemInfoTool()
}


def get_tool(name: str):

    return TOOLS[name]
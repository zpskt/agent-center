#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：executor.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 19:02 
@Description： 
'''
from app.tools.registry import get_tool


class ToolExecutor:

    async def execute(
        self,
        tool_name: str,
        **kwargs
    ):

        tool = get_tool(tool_name)

        return await tool.execute(
            **kwargs
        )
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_tool_registry.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 18:38 
@Description： 
'''
from app.tools.registry import get_tool


def test_get_system_info_tool():

    tool = get_tool(
        "system_info"
    )

    assert tool is not None

    assert tool.name == "system_info"
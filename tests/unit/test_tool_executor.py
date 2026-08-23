#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_tool_executor.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 19:06 
@Description： 
'''
import pytest

from app.tools.executor import ToolExecutor


@pytest.mark.asyncio
async def test_execute_system_info_tool():

    executor = ToolExecutor()

    result = await executor.execute(
        "system_info"
    )

    assert result is not None

    assert "cpu" in result
    assert "memory" in result
    assert "disk" in result
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_system_info_tool.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 18:36 
@Description： 
'''

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest

from app.tools.system_info import SystemInfoTool


@pytest.mark.asyncio
async def test_system_info_tool_execute():

    tool = SystemInfoTool()

    result = await tool.execute()

    assert result is not None

    assert "cpu" in result
    assert "memory" in result
    assert "disk" in result


@pytest.mark.asyncio
async def test_system_info_tool_metadata():

    tool = SystemInfoTool()

    assert tool.name == "system_info"

    assert tool.description is not None
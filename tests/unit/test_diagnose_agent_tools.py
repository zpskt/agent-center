#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_diagnose_agent_tools.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 19:10 
@Description： 
'''
import pytest

from app.agent.diagnose_agent import DiagnoseAgent
from app.domain.context import DiagnosisContext


@pytest.mark.asyncio
async def test_agent_contains_tools(
    fake_llm_client
):

    agent = DiagnoseAgent(
        llm_client=fake_llm_client
    )

    context = DiagnosisContext(
        user_id="user-001",
        conversation_id="conv-001",
        message="检查电脑",
        available_tools=[
            "system_info"
        ]
    )

    await agent.execute(context)

    assert "system_info" in fake_llm_client.last_prompt

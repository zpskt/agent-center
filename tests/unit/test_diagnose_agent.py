#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_diagnose_agent.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 08:35 
@Description： 
'''
import pytest

from app.agent.diagnose_agent import DiagnoseAgent
from app.domain.context import DiagnosisContext
from app.domain.exceptions import DiagnosisError
from app.infrastructure.llm.llm_client import LLMClient
from app.domain.models import  DiagnoseResponse

class InvalidLLMClient(LLMClient):

    async def invoke(self, prompt: str) -> str:
        return "这不是合法的 JSON"


@pytest.mark.asyncio
async def test_diagnose_agent(fake_llm_client):
    agent = DiagnoseAgent(
        llm_client=fake_llm_client
    )
    context = DiagnosisContext(
        user_id="user-001",
        conversation_id="conv-001",
        message="第二个问题",
        history=[
            {
                "role": "user",
                "content": "第一个问题",
            },
            {
                "role": "assistant",
                "content": "第一次回答",
            },
        ],
    )

    result = await agent.execute(context)

    assert "第一个问题" in fake_llm_client.last_prompt
    assert "第一次回答" in fake_llm_client.last_prompt
    assert "第二个问题" in fake_llm_client.last_prompt

    result = await agent.execute(context)

    assert isinstance(result, DiagnoseResponse)
    assert result.diagnosis == "测试诊断"
    assert result.confidence == 0.9
    assert result.recommendations == ["测试建议"]

@pytest.mark.asyncio
async def test_diagnose_agent_invalid_llm_response():
    agent = DiagnoseAgent(
        llm_client=InvalidLLMClient()
    )

    context = DiagnosisContext(
        user_id="user-001",
        conversation_id="conv-001",
        message="测试问题",
    )

    with pytest.raises(DiagnosisError):
        await agent.execute(context)
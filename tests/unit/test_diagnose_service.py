#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_diagnose_service.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 08:35 
@Description： 
'''
import pytest
from app.main import app

from app.agent.diagnose_agent import DiagnoseAgent
from app.infrastructure.llm.llm_client import LLMClient

class FakeLLMClient(LLMClient):

    async def invoke(self, prompt: str) -> str:
        return """
        {
            "diagnosis": "测试诊断",
            "confidence": 0.9,
            "recommendations": [
                "测试建议"
            ]
        }
        """

class InvalidLLMClient(LLMClient):

    async def invoke(self, prompt: str) -> str:
        return "这不是合法的 JSON"


@pytest.mark.asyncio
async def test_diagnose_service(fake_llm_client):
    from app.application.diagnose_service import DiagnoseService
    from app.domain.models import DiagnoseRequest

    agent = DiagnoseAgent(
        llm_client=fake_llm_client
    )

    service = DiagnoseService(agent=agent)

    request = DiagnoseRequest(
        user_id="user-001",
        message="测试问题",
    )

    result = await service.diagnose(request)

    assert result.diagnosis == "测试诊断"
    assert result.confidence == 0.9
    assert result.recommendations == ["测试建议"]

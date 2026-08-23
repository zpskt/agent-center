#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：conftest.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 08:53 
@Description： 
'''
import pytest

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

@pytest.fixture
def fake_llm_client():
    return FakeLLMClient()

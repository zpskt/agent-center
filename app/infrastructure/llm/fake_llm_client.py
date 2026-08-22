#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：fake_llm_client.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 21:49 
@Description： 
'''
from app.infrastructure.llm.llm_client import LLMClient


class FakeLLMClient(LLMClient):

    def invoke(self, prompt: str) -> str:
        return f"Fake LLM response: {prompt}"
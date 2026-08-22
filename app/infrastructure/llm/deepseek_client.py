#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：deepseek_client.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 22:00 
@Description： 
'''
from openai import OpenAI

from app.config.settings import settings
from app.infrastructure.llm.llm_client import LLMClient


class DeepSeekClient(LLMClient):

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""
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
from openai import AsyncOpenAI
from app.config.settings import settings
from app.infrastructure.llm.llm_client import LLMClient
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)

class DeepSeekClient(LLMClient):

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            timeout=settings.llm_timeout,
        )
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=5,
        ),
    )
    async def invoke(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""
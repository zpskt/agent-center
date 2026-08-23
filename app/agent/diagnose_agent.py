#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：diagnose_agent.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 21:03 
@Description： 
'''
from pydantic import ValidationError

from app.agent.prompts.diagnose_prompt import DIAGNOSE_SYSTEM_PROMPT
from app.domain.exceptions import DiagnosisError
from app.domain.models import DiagnoseResponse, DiagnosisContext
from app.infrastructure.llm.llm_client import LLMClient


class DiagnoseAgent:
    def __init__(self,llm_client: LLMClient):
        self.llm_client = llm_client
        self.prompt = ""

    async def execute(self, context: DiagnosisContext) -> DiagnoseResponse:
        history_text = "\n".join(
            f"{message.role}: {message.content}"
            for message in context.history
        )
        prompt = f"""
        {DIAGNOSE_SYSTEM_PROMPT}
        历史对话：
        {history_text}
        用户问题：
        {context.message}
        """

        result = await self.llm_client.invoke(prompt)
        try:
            return DiagnoseResponse.model_validate_json(result)
        except ValidationError as e:
            raise DiagnosisError("LLM 返回的诊断结果格式不正确") from e
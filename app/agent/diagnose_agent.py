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

from app.prompts.diagnose_prompt import DIAGNOSE_SYSTEM_PROMPT
from app.domain.exceptions import DiagnosisError, LLMResponseError
from app.domain.models import DiagnoseResponse, DiagnosisContext
from app.infrastructure.llm.llm_client import LLMClient
from app.prompts.diagnose_prompt import build_diagnose_prompt


class DiagnoseAgent:
    def __init__(self,llm_client: LLMClient):
        self.llm_client = llm_client
        self.prompt = ""

    def _build_prompt(self, context: DiagnosisContext):
        return build_diagnose_prompt(context)

    def parse_response(self, result: str) -> DiagnoseResponse:
        try:
            return DiagnoseResponse.model_validate_json(result)

        except ValidationError as e:
            raise LLMResponseError(
                "LLM response invalid"
            ) from e

    async def execute(self, context: DiagnosisContext) -> DiagnoseResponse:

        prompt = self._build_prompt(context)

        result = await self.llm_client.invoke(prompt)
        try:
            return self.parse_response(result)
        except ValidationError as e:
            raise DiagnosisError("LLM 返回的诊断结果格式不正确") from e
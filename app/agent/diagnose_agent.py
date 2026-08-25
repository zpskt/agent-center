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

from app.agent.base_agent import BaseAgent
from app.domain.context import DiagnosisContext
from app.domain.exceptions import DiagnosisError, LLMResponseError
from app.domain.models import DiagnoseResponse, AgentAction
from app.infrastructure.llm.llm_client import LLMClient
from app.prompts.diagnose import build_prompt
from app.prompts.registry import get_prompt


class DiagnoseAgent(BaseAgent):
    def parse_action(
            self,
            result: str
    ) -> AgentAction:
        """
        转换成意图
        """
        return AgentAction.model_validate_json(
            result
        )

    def build_prompt(self, context: DiagnosisContext):
        prompt_builder = get_prompt(
            "diagnose"
        )
        return prompt_builder(context)

    def parse_response(self, result: str) -> DiagnoseResponse:
        try:
            return DiagnoseResponse.model_validate_json(result)

        except ValidationError as e:
            raise LLMResponseError(
                "LLM response invalid"
            ) from e

    async def execute(self, context: DiagnosisContext) -> AgentAction:

        prompt = self.build_prompt(context)

        result = await self.llm_client.invoke(prompt)
        try:
            action = self.parse_action(result)
            if action.action == "final":
                if action.response is None:
                    raise DiagnosisError(
                        "最终诊断结果不能为空"
                    )

            return action

        except ValidationError as e:
            raise DiagnosisError(
                "LLM 返回的 AgentAction 格式不正确"
            ) from e
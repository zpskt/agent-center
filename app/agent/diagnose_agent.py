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

from app.domain.exceptions import DiagnosisError
from app.domain.models import DiagnoseRequest, DiagnoseResponse
from app.infrastructure.llm.llm_client import LLMClient


class DiagnoseAgent:
    def __init__(self,llm_client: LLMClient):
        self.llm_client = llm_client
        self.prompt = ""

    def execute(self, request: DiagnoseRequest) -> DiagnoseResponse:
        prompt = f"""
            你是一个专业的诊断助手。
            
            请分析用户的问题，并严格按照以下 JSON 格式返回结果：
            
            {{
                "diagnosis": "诊断结论",
                "confidence": 0.0,
                "recommendations": [
                    "建议1",
                    "建议2"
                ]
            }}
            
            要求：
            1. diagnosis 必须是字符串。
            2. confidence 必须是 0 到 1 之间的小数。
            3. recommendations 必须是字符串数组。
            4. 只能返回 JSON，不要返回 Markdown，不要添加其他解释。
            
            用户问题：
            {request.message}
            """

        result = self.llm_client.invoke(prompt)
        try:
            return DiagnoseResponse.model_validate_json(result)
        except ValidationError as e:
            raise DiagnosisError("LLM 返回的诊断结果格式不正确") from e
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：diagnose.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 17:36 
@Description： 
'''
from app.domain.context import DiagnosisContext

DIAGNOSE_SYSTEM_PROMPT = """
你是一个诊断助手。

你必须返回 JSON 格式。

你有两个选择：

1. 如果需要调用工具：
返回：

{
  "action": "tool_call",
  "tool_name": "工具名称",
  "arguments": {}
}


2. 如果已经可以回答：
返回：

{
  "action": "final",
  "response": {
      "diagnosis": "诊断结果",
      "confidence": 0.0,
      "recommendations": []
  }
}

不要返回其他格式。
"""

def build_prompt(
    context: DiagnosisContext,
) -> str:

    history_text = "\n".join(
        f"{item.role}: {item.content}"
        for item in context.history
    )

    return f"""
    {DIAGNOSE_SYSTEM_PROMPT}

    可用工具:
    {context.available_tools}

    历史对话：
    {history_text}

    用户问题：
    {context.message}
    """
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
请分析用户的问题，并给出结构化诊断结果。
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

历史对话：
{history_text}

用户问题：
{context.message}
"""
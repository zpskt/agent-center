#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：exceptions.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 22:21 
@Description： 
'''
class DiagnosisError(Exception):
    """诊断过程中发生的业务异常。"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class LLMResponseError(DiagnosisError):
    pass
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：llm_client.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 21:05 
@Description： 
'''
from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def invoke(self,prompt:str):
        return prompt
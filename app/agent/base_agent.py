#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：base_agent.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 18:23 
@Description： 
'''
from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, llm_client):
        self.llm_client = llm_client


    async def execute(self, context):
        prompt = self.build_prompt(context)

        result = await self.llm_client.invoke(prompt)

        return self.parse_response(result)


    @abstractmethod
    def build_prompt(self, context):
        pass


    @abstractmethod
    def parse_response(self, result):
        pass

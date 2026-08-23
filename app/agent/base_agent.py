#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：base_agent.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 18:23 
@Description： 负责所有agent统一流程
'''
from abc import ABC, abstractmethod

from app.domain.models import AgentAction


class BaseAgent(ABC):

    def __init__(self, llm_client):
        self.llm_client = llm_client


    async def execute(self, context):
        prompt = self.build_prompt(context)
        result = await self.llm_client.invoke(prompt)
        action = self.parse_action(result)

        if action.action == "final":
            return self.parse_response(result)

        if action.action == "tool_call":
            return await self.handle_tool_call(
                action
            )


    @abstractmethod
    def build_prompt(self, context):
        pass

    @abstractmethod
    def parse_action(
        self,
        result: str
    ) -> AgentAction:
        pass

    @abstractmethod
    def parse_response(
            self,
            result: str
    ):
        pass

    async def handle_tool_call(
        self,
        action: AgentAction
    ):
        raise NotImplementedError
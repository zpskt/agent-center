#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：base.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 18:35 
@Description： 
'''
from abc import ABC, abstractmethod


class BaseTool(ABC):

    name: str
    description: str
    parameters: dict = {}



    @abstractmethod
    async def execute(self, **kwargs):
        pass

    def get_schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description.strip(),
            "parameters": self.parameters,
        }
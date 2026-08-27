#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：tool_call_recorder.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/27 22:16 
@Description： 
'''
from abc import ABC, abstractmethod


class ToolCallRecorder(ABC):

    @abstractmethod
    async def start(
        self,
        run_id: int,
        tool_name: str,
        arguments: dict,
    ) -> int:
        pass

    @abstractmethod
    async def success(
        self,
        tool_call_id: int,
        result: dict,
    ) -> None:
        pass

    @abstractmethod
    async def fail(
        self,
        tool_call_id: int,
    ) -> None:
        pass
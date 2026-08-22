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
class LLMClient:
    def invoke(self,msg:str):
        return {"message": f"llm invoked: {msg}"}
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：health.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 17:35 
@Description： 
'''

from fastapi import FastAPI, APIRouter

router = APIRouter(prefix="/health")

@router.get('/')
def root():
    return {"status": "ok"}
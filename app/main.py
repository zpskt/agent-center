#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 17:26 
@Description： 
'''

from fastapi import FastAPI

from app.api.diagnose import router as diagnose_router
from app.api.health import router as health_router

app = FastAPI()

app.include_router(health_router)
app.include_router(diagnose_router)

@app.get('/')
def root():
    return {"message":"hello"}
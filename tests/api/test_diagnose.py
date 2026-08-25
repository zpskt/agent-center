#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_diagnose.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 08:35 
@Description： 
'''
import pytest
from starlette.testclient import TestClient
from app.main import app
from app.api.diagnose import get_llm_client
from app.infrastructure.llm.llm_client import LLMClient


def test_diagnose_api(fake_llm_client):
    app.dependency_overrides[get_llm_client] = lambda: fake_llm_client

    client = TestClient(app)

    response = client.post(
        "/diagnose/",
        json={
            "user_id": "user-001",
            "conversation_id": "conv-001",
            "message": "测试问题",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["diagnosis"] == "测试诊断"
    assert data["confidence"] == 0.9
    assert data["recommendations"] == ["测试建议"]

    app.dependency_overrides.clear()


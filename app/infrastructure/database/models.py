#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：models.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/26 23:38 
@Description： 
'''
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class ConversationModel(Base):
    __tablename__ = "conversation"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(64),
        index=True,
    )

    conversation_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class ConversationMessageModel(Base):
    __tablename__ = "conversation_message"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    conversation_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("conversation.conversation_id"),
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
    )

    content: Mapped[str] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

class AgentRunModel(Base):
    __tablename__ = "agent_run"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(64),
        index=True,
    )

    conversation_id: Mapped[str] = mapped_column(
        String(64),
        index=True,
    )

    agent_name: Mapped[str] = mapped_column(
        String(64),
    )

    status: Mapped[str] = mapped_column(
        String(32),
    )

    iterations: Mapped[int] = mapped_column(
        default=0,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

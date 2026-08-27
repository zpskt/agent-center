# agent-center
agent能力中心
## 启动
```shell
uv run uvicorn app.main:app --reload
```
执行测试脚本
```shell 
uv run pytest
```
文档地址：http://127.0.0.1:8000/docs
# Agent Center

一个基于 **FastAPI + Agent + LLM + Tool + Repository** 架构构建的 Agent 服务框架。

项目当前以“设备诊断”作为业务场景，但核心目标不是实现某一个具体诊断功能，而是提供一个可以持续扩展的 Agent 基础框架。

---

## 1. 项目定位

Agent Center 负责解决以下问题：

* 接收用户请求
* 管理多轮对话
* 调用 LLM
* 解析 Agent Action
* 自动执行 Tool
* 支持 Agent 多轮 Tool Calling Loop
* 持久化 Conversation
* 持久化 Agent Run
* 持久化 Tool Call
* 记录运行日志
* 通过依赖注入管理基础设施
* 允许替换 LLM、数据库、Repository 和 Tool

核心原则：

> **业务能力应该通过扩展实现，而不是不断修改 AgentRunner。**

---

# 2. 整体架构

```text
                           ┌──────────────────┐
                           │      FastAPI     │
                           │       API        │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ DiagnoseService  │
                           │ Application Layer │
                           └────────┬─────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
          ConversationRepo   AgentRunRepository   AgentRunner
                   │                                 │
                   │                                 │
                   ▼                                 ▼
             Conversation                         Agent
             Persistence                            │
                                                     ▼
                                                    LLM
                                                     │
                                                     ▼
                                               AgentAction
                                              /           \
                                             /             \
                                      tool_call           final
                                          │                 │
                                          ▼                 ▼
                                   ToolCallRecorder      Response
                                          │
                                          ▼
                                    ToolExecutor
                                          │
                                          ▼
                                        Tool
```

---

# 3. 核心模块职责

## 3.1 API Layer

位置：

```text
app/api/
```

负责：

* HTTP 请求
* FastAPI Dependency Injection
* Request / Response Model
* 调用 Application Service

API 层不应该：

* 直接调用 LLM
* 直接执行 Tool
* 直接操作数据库
* 编写 Agent Loop

例如：

```python
@router.post("/")
async def diagnose(
    request: DiagnoseRequest,
    service: DiagnoseService = Depends(get_diagnose_service),
):
    return await service.diagnose(request)
```

API 保持薄。

---

# 4. Application Layer

位置：

```text
app/application/
```

例如：

```text
DiagnoseService
```

负责业务流程编排：

```text
获取历史
    ↓
保存用户消息
    ↓
创建 DiagnosisContext
    ↓
创建 AgentRun
    ↓
调用 AgentRunner
    ↓
保存最终结果
    ↓
完成 AgentRun
```

Application Service 不负责：

* LLM API 具体实现
* Tool 具体实现
* SQLAlchemy 细节

这些都通过抽象接口注入。

---

# 5. Domain Layer

位置：

```text
app/domain/
```

这里定义核心业务对象和抽象能力。

例如：

```text
models.py
context.py
exceptions.py
repositories/
agent/
```

Domain 层应该尽量保持稳定。

典型结构：

```text
AgentAction
DiagnoseRequest
DiagnoseResponse
AgentRunResult
DiagnosisContext
ConversationMessage
ToolCallRecorder
ConversationRepository
```

Domain 不应该依赖：

```text
FastAPI
SQLAlchemy
OpenAI SDK
DeepSeek SDK
具体 Tool
```

---

# 6. AgentRunner

位置：

```text
app/agent/agent_runner.py
```

AgentRunner 是整个 Agent Loop 的核心调度器。

它负责：

```text
Agent.execute()
      ↓
AgentAction
      ↓
tool_call?
   ├── yes → ToolExecutor → tool_result → Agent.execute()
   │
   └── no → final
```

当前最大循环次数：

```python
MAX_ITERATIONS = 5
```

Runner 不应该关心：

* 具体是什么诊断能力
* Tool 是什么
* LLM 是 DeepSeek 还是 OpenAI
* 数据库是 SQLite 还是 PostgreSQL
* Tool 数据怎么存

Runner 只依赖抽象：

```text
BaseAgent
ToolExecutor
ToolCallRecorder
```

因此：

> **一般情况下，新增业务能力不应该修改 AgentRunner。**

---

# 7. 如何新增一个能力

例如现在已经有：

```text
system_info
```

如果需要增加：

```text
disk_health
```

推荐步骤如下。

---

## 7.1 创建 Tool

位置：

```text
app/tools/
```

例如：

```python
class DiskHealthTool(BaseTool):

    name = "disk_health"

    description = """
    检查当前系统磁盘健康状态。
    """

    async def execute(self, **kwargs):

        return {
            "status": "healthy",
            "temperature": 42,
        }
```

Tool 必须继承：

```python
BaseTool
```

并实现：

```python
async def execute(...)
```

---

# 8. 注册 Tool

修改：

```text
app/tools/registry.py
```

例如：

```python
from app.tools.disk_health import DiskHealthTool
from app.tools.system_info import SystemInfoTool


TOOLS = {
    "system_info": SystemInfoTool(),
    "disk_health": DiskHealthTool(),
}
```

这样：

```text
LLM
 ↓
action.tool_name = "disk_health"
 ↓
ToolExecutor
 ↓
get_tool("disk_health")
 ↓
DiskHealthTool
```

---

# 9. 是否需要修改 ToolExecutor？

通常不需要。

ToolExecutor 已经负责通用执行：

```python
tool = get_tool(tool_name)

return await tool.execute(
    **kwargs
)
```

因此新增 Tool 时：

> **只新增 Tool + Registry 注册，不修改 ToolExecutor。**

---

# 10. 是否需要修改 AgentRunner？

通常不需要。

AgentRunner 不应该出现：

```python
if tool_name == "system_info":
    ...

if tool_name == "disk_health":
    ...
```

这种代码。

如果出现这种代码，说明 Tool 层和 Runner 耦合了。

正确结构应该始终是：

```text
AgentRunner
     ↓
ToolExecutor
     ↓
ToolRegistry
     ↓
具体 Tool
```

---

# 11. 新增 Tool 是否需要修改 Prompt？

如果 LLM 需要知道这个 Tool 的存在，需要。

例如：

```text
可用工具：

system_info:
获取当前系统 CPU、内存、磁盘信息。

disk_health:
检查磁盘健康状态。
```

推荐由 Context 动态提供：

```python
context.available_tools
```

而不是把 Tool 名称全部硬编码在 AgentRunner。

最终目标：

```text
Tool Registry
      ↓
Available Tools
      ↓
Prompt
      ↓
LLM
```

这样新增 Tool 后，Prompt 能自动知道新能力。

---

# 12. 新增 Tool 的完整流程

以后新增业务能力，按照下面流程：

```text
1. 创建 BaseTool 子类
        ↓
2. 实现 execute()
        ↓
3. 设置 name
        ↓
4. 设置 description
        ↓
5. 注册到 Tool Registry
        ↓
6. 确保 Prompt 能看到 Tool
        ↓
7. 编写 Tool 单元测试
        ↓
8. 编写 Agent Tool Calling 测试
        ↓
9. 调用真实 API 验证
```

一般不需要修改：

```text
AgentRunner
DiagnoseService
ToolExecutor
```

---

# 13. 如何新增 LLM

LLM 是基础设施，不应该直接写死在 Agent 中。

当前结构：

```text
BaseAgent
   ↓
LLMClient
   ↑
   ├── DeepSeekClient
   └── FakeLLMClient
```

LLM 抽象：

```python
class LLMClient(ABC):

    @abstractmethod
    async def invoke(self, prompt: str) -> str:
        pass
```

---

# 14. 新增一个 LLM Provider

例如增加 OpenAI。

创建：

```text
app/infrastructure/llm/openai_client.py
```

实现：

```python
class OpenAIClient(LLMClient):

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            timeout=settings.llm_timeout,
        )

    async def invoke(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""
```

关键要求：

> Agent 不允许直接依赖 OpenAI / DeepSeek SDK。

Agent 只依赖：

```python
LLMClient
```

---

# 15. 新增 LLM 后需要修改什么？

通常修改：

```text
settings.py
.env
DI Provider
新的 LLM Client
```

例如：

```text
LLM_PROVIDER=deepseek
```

以后可以：

```text
LLM_PROVIDER=openai
```

然后在 DI 层：

```python
def get_llm_client() -> LLMClient:

    if settings.llm_provider == "deepseek":
        return DeepSeekClient()

    if settings.llm_provider == "openai":
        return OpenAIClient()

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )
```

这样 Agent 完全不需要修改。

---

# 16. Settings 原则

所有环境相关配置统一进入：

```text
app/config/settings.py
```

例如：

```python
class Settings(BaseSettings):

    llm_api_key: str
    llm_model: str
    llm_base_url: str
    llm_timeout: int

    database_url: str

    log_level: str = "INFO"
```

`.env`：

```text
LLM_API_KEY=xxx
LLM_MODEL=xxx
LLM_BASE_URL=xxx
LLM_TIMEOUT=60

DATABASE_URL=sqlite+aiosqlite:///./agent_center.db

LOG_LEVEL=INFO
```

代码中：

```python
from app.config.settings import settings
```

禁止在业务代码里硬编码：

```python
"sqlite:///..."
"https://api.xxx.com"
"sk-xxxxx"
```

---

# 17. 如何更换数据库

数据库属于 Infrastructure。

例如当前：

```text
SQLite
    ↓
SQLAlchemy Async
```

以后可以切换：

```text
PostgreSQL
    ↓
SQLAlchemy Async
```

核心业务代码原则上不应该改变。

---

# 18. Database Layer

位置：

```text
app/infrastructure/database/
```

负责：

* Engine
* Session
* ORM Model
* Database 初始化

例如：

```text
database.py
models.py
```

---

# 19. Database URL 必须来自 Settings

例如：

```python
from sqlalchemy.ext.asyncio import create_async_engine

from app.config.settings import settings


engine = create_async_engine(
    settings.database_url,
)
```

不要：

```python
engine = create_async_engine(
    "sqlite+aiosqlite:///./agent_center.db"
)
```

这样以后切 PostgreSQL，只需要修改：

```text
DATABASE_URL
```

---

# 20. Repository Pattern

业务代码不应该直接操作 SQLAlchemy。

错误：

```python
result = await session.execute(...)
```

直接写在：

```text
DiagnoseService
AgentRunner
```

正确：

```text
Application
    ↓
Repository Interface
    ↓
Repository Implementation
    ↓
SQLAlchemy
```

例如：

```text
ConversationRepository
        ↑
MemoryConversationRepository
        ↑
DatabaseConversationRepository
```

---

# 21. Conversation 持久化

Domain 定义：

```python
class ConversationRepository(ABC):
    ...
```

Infrastructure 实现：

```text
app/infrastructure/conversation/
```

当前可以有：

```text
MemoryConversationRepository
DatabaseConversationRepository
```

这样测试时：

```text
MemoryConversationRepository
```

生产环境：

```text
DatabaseConversationRepository
```

Application Service 不需要知道底层是哪一个。

---

# 22. AgentRun 持久化

一次 Agent 执行对应一个：

```text
AgentRun
```

例如：

```text
agent_run
----------------------------
id
user_id
conversation_id
agent_name
status
iterations
started_at
finished_at
error
```

生命周期：

```text
create
  ↓
running
  ↓
success
```

异常：

```text
create
  ↓
running
  ↓
failed
```

---

# 23. ToolCall 持久化

每一次 Tool 调用对应一个：

```text
ToolCall
```

例如：

```text
tool_call
----------------------------
id
run_id
tool_name
arguments
result
status
started_at
finished_at
```

关系：

```text
AgentRun
   │
   ├── ToolCall
   ├── ToolCall
   └── ToolCall
```

`run_id` 用于追踪这些 Tool 调用属于哪一次 Agent 执行。

---

# 24. ToolCallRecorder

AgentRunner 不应该直接依赖：

```text
ToolCallRepository
```

而应该依赖：

```text
ToolCallRecorder
```

Domain：

```python
class ToolCallRecorder(ABC):
    ...
```

Infrastructure：

```text
ToolCallRepository
```

测试：

```text
FakeToolCallRecorder
```

依赖关系：

```text
                 ToolCallRecorder
                  /            \
                 /              \
ToolCallRepository          FakeToolCallRecorder
        │
        ↓
    SQLAlchemy
```

这样 AgentRunner 完全不关心数据库。

---

# 25. 如果更换数据库，需要改什么？

例如：

```text
SQLite → PostgreSQL
```

主要修改：

```text
.env
database.py
数据库迁移
```

如果使用 SQLAlchemy，Repository 通常不需要改变。

例如：

```text
DATABASE_URL=
sqlite+aiosqlite://...
```

修改成：

```text
DATABASE_URL=
postgresql+asyncpg://...
```

Application Layer：

```text
不改
```

Agent Layer：

```text
不改
```

Tool Layer：

```text
不改
```

---

# 26. 新增持久化表

例如以后需要记录：

```text
LLMCall
```

推荐流程：

```text
1. Domain 定义需要记录的能力
        ↓
2. 创建 Repository / Recorder 抽象
        ↓
3. Infrastructure 创建 ORM Model
        ↓
4. 实现 Repository
        ↓
5. DI 注入
        ↓
6. 在对应 Application / Agent 流程中调用
```

不要直接在 AgentRunner 里创建：

```python
LLMCallModel(...)
```

否则 AgentRunner 会与数据库强耦合。

---

# 27. 日志

日志负责：

> “程序运行时发生了什么？”

数据库负责：

> “业务执行结果是什么？”

二者不要混淆。

当前日志：

```text
app/infrastructure/logging/
```

统一通过：

```python
logger = get_logger(__name__)
```

使用。

---

# 28. 日志应该记录什么？

推荐：

```text
Agent run started
Agent iteration started
Agent action received
Tool call started
Tool call completed
Tool call failed
Agent run completed
Agent run failed
```

并带关键上下文：

```text
run_id
conversation_id
iteration
tool_name
tool_call_id
```

例如：

```text
Agent action received |
run_id=123 |
iteration=2 |
action=tool_call
```

---

# 29. 日志不要记录什么？

不要直接记录：

```text
API Key
Authorization Header
完整敏感用户数据
密码
Token
```

LLM Prompt / Response 如果未来需要记录，建议：

```text
DEBUG
```

并进行脱敏或截断。

生产环境不要默认输出完整 Prompt。

---

# 30. 测试策略

项目测试分成三层。

## Tool Test

测试 Tool 本身：

```text
test_system_info.py
test_disk_health.py
```

验证：

```text
Tool 输入
Tool 输出
异常行为
```

---

## AgentRunner Test

测试：

```text
tool_call
    ↓
ToolExecutor
    ↓
tool_result
    ↓
final
```

使用：

```text
FakeAgent
FakeToolExecutor
FakeToolCallRecorder
```

不依赖真实数据库。

---

## API Test

测试完整 HTTP 链路：

```text
HTTP
 ↓
FastAPI
 ↓
DI
 ↓
Service
 ↓
Agent
 ↓
LLM
 ↓
Response
```

测试时通过：

```python
app.dependency_overrides
```

替换真实 LLM。

---

# 31. 测试环境原则

单元测试不要依赖：

```text
真实 LLM
真实数据库
真实操作系统状态
真实网络
```

应该使用：

```text
FakeLLMClient
FakeToolExecutor
FakeToolCallRecorder
MemoryRepository
```

这样测试：

```text
快
稳定
可重复
```

---

# 32. 新增能力时的修改清单

以后新增一个 Tool，可以直接按照这个 Checklist：

```text
□ 创建 xxx_tool.py

□ 继承 BaseTool

□ 实现 execute()

□ 定义 name

□ 定义 description

□ 注册到 registry.py

□ 确保 available_tools 能暴露该 Tool

□ 必要时修改 Agent Prompt

□ 编写 Tool 单元测试

□ 编写 Tool Calling 测试

□ 调用 API 验证

□ 检查 AgentRun

□ 检查 ToolCall
```

通常不需要修改：

```text
□ AgentRunner
□ ToolExecutor
□ DiagnoseService
```

---

# 33. 新增 LLM 时的修改清单

```text
□ 创建新的 LLMClient 实现

□ 继承 LLMClient

□ 实现 invoke()

□ 增加 Settings 配置

□ 增加 .env 配置

□ 修改 DI Provider

□ 编写 Fake / Unit Test

□ 验证 Agent 不需要修改
```

核心目标：

```text
Agent
  ↓
LLMClient
  ↑
DeepSeekClient
OpenAIClient
OtherClient
```

---

# 34. 更换数据库时的修改清单

```text
□ 修改 DATABASE_URL

□ 确认数据库 Driver

□ 更新数据库初始化配置

□ 执行数据库迁移

□ 验证 Repository

□ 执行 Integration Test
```

原则：

```text
Application Layer 不改
Agent Layer 不改
Tool Layer 不改
```

---

# 35. 架构演进原则

以后项目越来越复杂时，遵循以下原则。

### 原则一：新增能力优先扩展，不修改核心循环

优先：

```text
新增 Tool
新增 Agent
新增 Repository
新增 LLMClient
```

而不是：

```text
修改 AgentRunner
```

---

### 原则二：依赖抽象，不依赖实现

正确：

```python
def __init__(
    self,
    llm_client: LLMClient,
):
```

错误：

```python
def __init__(
    self,
    deepseek_client: DeepSeekClient,
):
```

---

### 原则三：基础设施不能污染 Domain

Domain 不应该出现：

```python
from sqlalchemy import ...
from fastapi import ...
from openai import ...
```

---

### 原则四：Runner 负责调度，不负责业务

Runner 只负责：

```text
执行 Agent
判断 Action
调用 Tool
循环
限制最大迭代次数
```

不要让 Runner 负责：

```text
设备诊断逻辑
数据库 SQL
HTTP
具体 Tool 判断
```

---

### 原则五：Service 负责业务流程

Service 负责：

```text
Request
 ↓
History
 ↓
Context
 ↓
AgentRun
 ↓
Runner
 ↓
Response
 ↓
Persistence
```

---

# 36. 当前推荐目录结构

```text
app/
├── api/
│   └── diagnose.py
│
├── agent/
│   ├── base_agent.py
│   ├── agent_runner.py
│   └── diagnose_agent.py
│
├── application/
│   └── diagnose_service.py
│
├── config/
│   └── settings.py
│
├── domain/
│   ├── agent/
│   │   └── tool_call_recorder.py
│   │
│   ├── context.py
│   ├── exceptions.py
│   ├── models.py
│   └── repositories/
│       └── conversation_repository.py
│
├── infrastructure/
│   ├── agent/
│   │   └── tool_call_repository.py
│   │
│   ├── conversation/
│   │   ├── conversation_repository.py
│   │   ├── memory_conversation_repository.py
│   │   └── database_conversation_repository.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── llm/
│   │   ├── llm_client.py
│   │   ├── deepseek_client.py
│   │   └── fake_llm_client.py
│   │
│   └── logging/
│       └── logger.py
│
├── tools/
│   ├── base.py
│   ├── executor.py
│   ├── registry.py
│   └── system_info.py
│
└── main.py
```

---

# 37. 一句话判断“应该改哪里”

以后遇到需求，可以先问：

### “这是一个新的能力吗？”

是：

```text
Tool
```

### “这是一个新的 LLM Provider 吗？”

是：

```text
LLMClient implementation
```

### “这是一个新的数据库存储方式吗？”

是：

```text
Repository implementation
```

### “这是一次 Agent 执行过程的调度问题吗？”

才考虑：

```text
AgentRunner
```

### “这是业务流程变化吗？”

考虑：

```text
Application Service
```

### “这是 HTTP 接口变化吗？”

考虑：

```text
API Layer
```

---

# 38. 最重要的扩展规则

整个项目最终希望达到这样的状态：

```text
                    Agent Framework
                         │
          ┌──────────────┼──────────────┐
          │              │              │
         LLM            Tool         Persistence
          │              │              │
     ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
  DeepSeek   OpenAI  SystemInfo DiskHealth SQLite PostgreSQL
```

增加一个能力：

```text
+ NewTool
```

增加一个 LLM：

```text
+ NewLLMClient
```

增加一个数据库：

```text
+ NewRepository
```

而核心：

```text
AgentRunner
DiagnoseService
ToolExecutor
```

尽量保持不变。

这就是这个项目最核心的架构目标：

> **让业务能力增长，而不是让核心框架越来越复杂。**

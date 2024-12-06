# 🦁 Lion Framework
> Language InterOperable Network
>
> A powerful Python framework for structured AI conversations and operations

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/lion-os.svg)](https://badge.fury.io/py/lion-os)
![PyPI - Downloads](https://img.shields.io/pypi/dm/lion-os?color=blue)

## 🌟 Features

- 🎯 Dynamic structured output at runtime
- 🔄 Easy composition of multi-step processes
- 🤖 Support for any model via `litellm`
- 🏗️ Built-in conversation management
- 🧩 Extensible architecture
- 🔍 Type-safe with Pydantic models

## 🚀 Quick Install

```bash
pip install lion-os
```

## Note

the `operation` API is experimental and may change in future versions. Use with caution.


## 💡 Usage Examples

### 1️⃣ Simple Communication

using litellm integration
```python
from lion import LiteiModel, Branch

# Initialize model and branch
imodel = LiteiModel(
    model="openai/gpt-4o",
    api_key="OPENAI_API_KEY",
    temperature=0.2,
)
branch = Branch(imodel=imodel)

# Basic communication
result = await branch.communicate(
    instruction="Give me ideas for FastAPI interview questions",
    context="We're hiring senior engineers"
)
```

using lion's own service system (only supports openai / anthropic / perplexity)
```python
from lion import iModel

# Initialize model and branch
imodel = iModel(
    provider="openai",
    model="gpt-4o",
    api_key="OPENAI_API_KEY",
    temperature=0.2,
    task="chat",
)

# if use anthropic
# imodel = iModel(
#     provider="anthropic",
#     model="claude-3-5-sonnet-20241022",
#     task="messages",
#     api_key="ANTHROPIC_API_KEY",
#     max_tokens=500,
# )

# use perplexity
# imodel = iModel(
#     provider="perplexity",
#     model="llama-3.1-sonar-small-128k-online",
#     task="chat/completions",
#     api_key="PERPLEXITY_API_KEY",
#     max_tokens=500,
# )

branch = Branch(imodel=imodel)

# Basic communication
result = await branch.communicate(
    instruction="Give me ideas for FastAPI interview questions",
    context="We're hiring senior engineers"
)
```


### 2️⃣ Structured Output with Pydantic

```python
from pydantic import BaseModel

class CodingQuestion(BaseModel):
    question: str
    evaluation_criteria: str

# Get structured responses
questions = await branch.operate(
    instruction="Generate FastAPI coding questions",
    context="Technical interview context",
    operative_model=CodingQuestion
)
```

### 3️⃣ Advanced Operations (Brainstorming)

```python
from lion.operations import brainstorm

result = await brainstorm(
    instruct={
        "instruction": "Design API endpoints for a todo app",
        "context": "Building a modern task management system"
    },
    imodel=imodel,
    num_instruct=3,
    operative_model=CodingQuestion,
    auto_run=True
)
```

## 🎯 Key Components

| Component | Description |
|-----------|-------------|
| Branch | Main conversation controller |
| MessageManager | Handles message flow and history |
| ToolManager | Manages function execution and tools |
| Operative | Structures operations and responses |


### Requirements

python 3.11+ required

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=lion-agi/lion-os&type=Date)](https://star-history.com/#ohdearquant/lion-os)

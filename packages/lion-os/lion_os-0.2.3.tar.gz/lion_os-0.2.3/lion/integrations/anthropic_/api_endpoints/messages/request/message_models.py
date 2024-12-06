from typing import List, Literal, Optional, TypeAlias

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant"] = Field(
        description="The role of the message sender"
    )
    content: str = Field(description="The content of the message")

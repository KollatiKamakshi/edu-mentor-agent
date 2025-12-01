from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import time

class A2AMessage(BaseModel):
    """Structured message for Agent-to-Agent (A2A) communication."""
    sender: str = Field(..., description="The name of the sending agent.")
    recipient: str = Field(..., description="The name of the intended receiving agent.")
    task_id: str = Field(..., description="A unique identifier for the specific task/exchange.")
    timestamp: float = Field(default_factory=time.time, description="Timestamp of message creation.")
    content: Dict[str, Any] = Field(..., description="The core payload of the message (task or result).")
    session_id: str = Field(..., description="The persistent ID for the user's session.")

class Protocol:
    """Handles the creation and passing of structured messages."""

    @staticmethod
    def create_message(sender: str, recipient: str, content: Dict[str, Any], session_id: str, task_id: Optional[str] = None) -> A2AMessage:
        if task_id is None:
            task_id = f"{sender}_{recipient}_{int(time.time() * 1000)}"
        return A2AMessage(
            sender=sender,
            recipient=recipient,
            task_id=task_id,
            content=content,
            session_id=session_id
        )

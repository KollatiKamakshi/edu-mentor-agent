import logging
import json # <-- CRITICAL FIX: Import JSON library
from typing import Dict, Any
from project.core.a2a_protocol import A2AMessage
from project.tools.tools import Tool

class BaseAgent:
    """Base class providing common structure and LLM mocking capabilities."""

    def __init__(self, name: str, system_prompt: str, tools: Dict[str, Tool] = None):
        self.name = name
        self.logger = logging.getLogger(name)
        self.system_prompt = system_prompt
        self.tools = tools if tools is not None else {}

    def _mock_llm_call(self, prompt: str) -> str:
        """
        A function to simulate the behavior of an LLM.
        In a real project, this would be an API call (e.g., OpenAI, Anthropic).
        """
        self.logger.debug(f"Simulating LLM call with prompt: {prompt[:100]}...")

        if "decompose" in prompt.lower() and self.name == "Planner":
            # Planner mock response
            return json.dumps([
                {"topic": "Python Variables and Types", "resource_type": "Video"},
                {"topic": "Basic Control Flow (If/Else)", "resource_type": "Article"},
                {"topic": "Writing Your First Function", "resource_type": "Quiz"}
            ])

        elif "summarize" in prompt.lower() and self.name == "Worker":
             # Worker mock response for summarization
             return f"The worker found this resource on: {prompt.split('topic: ')[-1].split('\\n')[0]}."

        elif "vet the following" in prompt.lower() and self.name == "Evaluator":
            # Evaluator mock response
            return json.dumps({
                "quality_score": 4.5,
                "validated": True,
                "notes": "Resource is recent and highly relevant."
            })

        return f"[{self.name} Mock Output]: Processed message content."

    def handle_message(self, message: A2AMessage) -> A2AMessage:
        """Processes an incoming A2A message and returns a reply message."""
        raise NotImplementedError

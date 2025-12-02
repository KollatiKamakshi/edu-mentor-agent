import logging
import os
import uuid
from typing import Dict, Any, Optional

# Import Core Components
from project.core.a2a_protocol import A2AMessage, Protocol
from project.memory.session_memory import SessionMemory

# Import Agents
from project.agents.planner import Planner
from project.agents.worker import Worker
from project.agents.evaluator import Evaluator

from project.tools.tools import GoogleSearchTool, RealTextSummarizerTool, RealDataExtractorTool
from project.tools.llm_tool import LLMTool

# Setup logger
main_agent_logger = logging.getLogger("MainAgent")

class MainAgent:
    """
    The central router that orchestrates the flow of messages between specialized agents.
    """
    def __init__(self):
        main_agent_logger.info("MainAgent initialized all components.")
        self.logger = main_agent_logger

        # In MainAgent.__init__
        google_api_key: Optional[str] = os.environ.get("GOOGLE_API_KEY")
        google_cx_id: Optional[str] = os.environ.get("GOOGLE_CX_ID")
        huggingface_api_key: Optional[str] = os.environ.get("HUGGINGFACE_API_KEY")
        # print("--- API Key Debug Check ---")
        # print(f"GOOGLE_API_KEY length: {len(google_api_key) if google_api_key else 0}")
        # print(f"GOOGLE_CX_ID length: {len(google_cx_id) if google_cx_id else 0}")
        # print(f"HUGGINGFACE_API_KEY length: {len(huggingface_api_key) if huggingface_api_key else 0}")
       
        # 1. Initialize Memory
        self.memory = SessionMemory()

        # 2. Initialize Tools
        self.tools = {
            "search": GoogleSearchTool(google_api_key, google_cx_id),
            "summarizer": RealTextSummarizerTool(huggingface_api_key),
            "llm": LLMTool(google_api_key),
            "extractor": RealDataExtractorTool() # Add the extractor tool here
        }
        self.logger.info(f"MainAgent initialized with tools: {list(self.tools.keys())}") # ADDED LOGGING

        # 3. Initialize Agents
        self.agents = {
            "Planner": Planner(self.memory, self.tools['llm']),
            "Worker": Worker(self.tools),
            "Evaluator": Evaluator(),
        }

        self.agent_map = {name: agent for name, agent in self.agents.items()}
        self.agent_map['MainAgent'] = self

    def handle_message(self, user_input: str) -> Dict[str, Any]:
        session_id = str(uuid.uuid4())
        self.logger.info(f"Starting new session {session_id} for input: '{user_input}'")

        current_message = Protocol.create_message(
            "MainAgent",
            "Planner",
            {"user_input": user_input},
            session_id
        )

        final_output = None
        step = 0

        while current_message.recipient != "MainAgent" or final_output is None:
            step += 1
            sender = current_message.sender
            recipient = current_message.recipient

            self.logger.info(f"\n[STEP {step}] Routing message: {sender} -> {recipient}")

            if recipient not in self.agent_map:
                self.logger.error(f"Unknown recipient: {recipient}")
                return {"error": f"Unknown agent recipient: {recipient}"}

            recipient_agent = self.agent_map[recipient]
            reply_message = recipient_agent.handle_message(current_message)

            if reply_message.recipient == "MainAgent":
                final_output = reply_message.content

            current_message = reply_message

        return final_output

def run_agent(user_input: str) -> Dict[str, Any]:
    import os
    import uuid
    from project.tools.tools import GoogleSearchTool, RealTextSummarizerTool, RealDataExtractorTool
    from project.tools.llm_tool import LLMTool

    agent = MainAgent()
    return agent.handle_message(user_input)

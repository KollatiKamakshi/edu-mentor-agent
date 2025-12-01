import logging
from typing import Dict, Any, List
from project.core.a2a_protocol import A2AMessage, Protocol
from project.memory.session_memory import SessionMemory
from project.tools.llm_tool import LLMTool # New Import

# Setup logger
planner_logger = logging.getLogger("Planner")

class Planner:
    """
    Decomposes the user's learning goal into sub-topics and assembles the final learning path.
    """
    def __init__(self, memory: SessionMemory, llm_tool: LLMTool): # Added llm_tool argument
        planner_logger.info("Planner agent initialized.")
        self.logger = planner_logger
        self.memory = memory
        self.goal_store: Dict[str, str] = {}
        self.llm_tool = llm_tool # Store the new tool

    def _decompose_goal(self, user_input: str) -> List[Dict[str, str]]:
        """
        Uses the LLM Tool to dynamically decompose the user goal into structured topics.
        """
        self.logger.info(f"Received user goal: '{user_input}'")

        # --- THE PERMANENT SOLUTION: CALLING THE LLM TOOL ---
        # The LLMTool will handle the call to Gemini or fallback to mock logic
        topics = self.llm_tool.decompose(user_input)

        self.logger.info(f"Decomposed goal into {len(topics)} sub-topics. Delegating to Worker.")
        return topics

    def _determine_skill_level(self, session_id: str) -> str:
        # For simplicity, always returns 'Beginner' for the initial demo
        return "Beginner"

    def handle_message(self, message: A2AMessage) -> A2AMessage:

        if 'user_input' in message.content:
            # --- STEP 1: DECOMPOSITION (MainAgent -> Planner) ---
            user_input = message.content['user_input']
            self.goal_store[message.session_id] = user_input

            topics = self._decompose_goal(user_input)

            return Protocol.create_message(
                "Planner",
                "Worker",
                {"topics": topics},
                message.session_id
            )

        elif 'validated_resources' in message.content:
            # --- STEP 4: ASSEMBLE (Evaluator -> Planner) ---
            validated_resources: List[Dict[str, Any]] = message.content['validated_resources']
            self.logger.info(f"Received {len(validated_resources)} validated resources from Evaluator. Assembling final path.")

            # 1. Update Memory (Simulated)
            skill_level = self._determine_skill_level(message.session_id)
            self.memory.update_user_skill(message.session_id, skill_level)
            self.logger.info(f"Updated memory for user {message.session_id}. New skill: {skill_level}")

            # 2. Assemble Final Response to MainAgent
            final_goal = self.goal_store.get(message.session_id, "Unknown Goal")

            return Protocol.create_message(
                "Planner",
                "MainAgent",
                {
                    "main_goal": final_goal,
                    "validated_path": validated_resources
                },
                message.session_id
            )

        return Protocol.create_message(
            "Planner",
            "MainAgent",
            {"error": "Planner received unexpected message content."},
            message.session_id
        )

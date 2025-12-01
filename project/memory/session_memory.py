import logging
from typing import Dict, Any

memory_logger = logging.getLogger("SessionMemory")

class SessionMemory:
    """
    Simulated memory store for tracking session state and user skill progression.
    """
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        memory_logger.info("SessionMemory initialized.")

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Retrieves data for a specific session ID."""
        return self.sessions.get(session_id, {})

    def update_session(self, session_id: str, data: Dict[str, Any]):
        """Updates or creates data for a session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        self.sessions[session_id].update(data)
        memory_logger.debug(f"Session {session_id} updated.")

    def update_user_skill(self, session_id: str, new_skill_level: str):
        """
        FIX: Implements the method the Planner agent expects to call.
        Simulates updating the user's skill level or history.
        """
        # We don't actually need to store it for the demo, just ensure the method exists
        # so the Planner can call it without crashing.
        self.update_session(session_id, {"skill_level": new_skill_level})
        memory_logger.info(f"Updated memory for user {session_id}. New skill: {new_skill_level}")

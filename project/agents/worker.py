import logging
from typing import Dict, Any, List
from project.core.a2a_protocol import A2AMessage, Protocol

# Setup logger
worker_logger = logging.getLogger("Worker")

class Worker:
    """
    Handles tool calls (search, extraction, summarization) to fulfill Planner's requests.
    """
    # List of low-quality or non-extractable domains to skip

    def __init__(self, tools: Dict[str, Any]):
        # FIX: Define the 'name' attribute
        self.name = "Worker"

        worker_logger.info("Worker agent initialized.")
        self.logger = worker_logger
        self.tools = tools
        self.logger.info(f"Worker received tools: {list(self.tools.keys())}") # ADDED LOGGING

    def _process_topic(self, topic_info: Dict[str, str]) -> Dict[str, Any]:
        """Runs the search -> extraction -> summarization workflow for a single topic."""
        topic = topic_info['topic']
        content_type = topic_info['type']

        # 1. Search for Resource
        search_results = self.tools['search'].execute(topic, content_type=content_type, max_results=1)

        if not search_results:
            self.logger.warning(f"No resource found for topic: {topic}")
            return None

        resource = search_results[0]
        resource['topic'] = topic # Add topic back for the Planner/Evaluator

        # 2. Extract Content
        extracted_content = self.tools['extractor'].execute(resource['link'])

        # 3. Summarize Content
        resource['summary'] = self.tools['summarizer'].execute(extracted_content)

        return resource

    def handle_message(self, message: A2AMessage) -> A2AMessage:
        content = message.content
        session_id = message.session_id

        topics: List[Dict[str, str]] = content.get("topics", [])
        self.logger.info(f"Received {len(topics)} sub-topics for processing.")

        processed_resources = []
        for topic_info in topics:
            resource = self._process_topic(topic_info)
            if resource:
                processed_resources.append(resource)

        self.logger.info(f"Finished processing. Sending {len(processed_resources)} results to Evaluator.")

        # Now self.name is correctly defined
        return Protocol.create_message(
            self.name,
            "Evaluator",
            {"resources": processed_resources},
            session_id,
            task_id=message.task_id
        )

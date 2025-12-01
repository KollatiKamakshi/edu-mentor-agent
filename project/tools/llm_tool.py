import logging
from typing import Optional, Any, Dict, List
import json

# Setup logger
llm_logger = logging.getLogger("LLMTool")

class LLMTool:
    """
    Tool to perform complex reasoning tasks like goal decomposition using an LLM.
    Uses MOCK logic if the Gemini API is not available or key is missing.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.name = "LLM Decomposition Tool"
        self.api_key = api_key
        self.client = None

        # Check for real API key and attempt to initialize the real client
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                llm_logger.info("LLMTool initialized with real Gemini Client.")
            except ImportError:
                llm_logger.warning("Google GenAI SDK not found. Using MOCK LLM Tool.")
                self.api_key = None
            except Exception as e:
                llm_logger.error(f"Error initializing Gemini Client: {e}. Using MOCK LLM Tool.")
                self.api_key = None

        if not self.api_key:
             llm_logger.warning("Using MOCK LLM Tool.")

    def _mock_decompose(self, user_input: str) -> List[Dict[str, str]]:
        """Fallback to the hardcoded logic you were using."""
        normalized_input = user_input.lower()

        # This is the last version of your robust mock logic
        if "python" in normalized_input:
            topics = [{"topic": "Python Variables and Types", "type": "Video"}, {"topic": "Basic Control Flow (If/Else)", "type": "Article"}, {"topic": "Writing Your First Function", "type": "Quiz"}]
        elif "javascript" in normalized_input:
            if "advanced" in normalized_input:
                topics = [{"topic": "JavaScript Design Patterns and Modules", "type": "Article"}, {"topic": "Advanced Reactivity and State Management", "type": "Video"}, {"topic": "Deep Dive into the Event Loop", "type": "Quiz"}]
            else:
                topics = [{"topic": "JavaScript Variables and Data Types", "type": "Article"}, {"topic": "DOM Manipulation Basics", "type": "Video"}, {"topic": "Asynchronous JavaScript (Promises)", "type": "Quiz"}]
        elif "dsa" in normalized_input or "data structures" in normalized_input or "algorithms" in normalized_input:
            if "advanced" in normalized_input:
                topics = [{"topic": "Advanced Dynamic Programming", "type": "Article"}, {"topic": "Graph Algorithms (e.g., Dijkstra's, A*)", "type": "Video"}, {"topic": "Complex Tree Structures (e.g., Red-Black Trees)", "type": "Quiz"}]
            else:
                topics = [{"topic": "Introduction to Arrays and Linked Lists", "type": "Video"}, {"topic": "Sorting Algorithms (e.g., Merge Sort, Quick Sort)", "type": "Article"}, {"topic": "Understanding Stacks and Queues", "type": "Quiz"}]
        elif "cloud" in normalized_input:
            topics = [{"topic": "Cloud Computing Fundamentals (IaaS, PaaS, SaaS)", "type": "Video"}, {"topic": "Introduction to AWS EC2 and S3", "type": "Article"}, {"topic": "Basic Networking Concepts in the Cloud", "type": "Quiz"}]
        else:
            topics = [{"topic": "General Programming Principles", "type": "Video"}]

        return topics

    def decompose(self, user_input: str) -> List[Dict[str, str]]:
        """Executes the goal decomposition using the real LLM or the mock logic."""

        if not self.client:
            return self._mock_decompose(user_input)

        try:
            # The prompt is designed to enforce a specific, parsable JSON structure
            prompt = (
                f"The user wants to learn: '{user_input}'. "
                "Decompose this goal into exactly 3 diverse and sequential sub-topics. "
                "For each topic, suggest the best content type from: Video, Article, Quiz. "
                "Respond ONLY with a JSON list in the format: "
                "[{'topic': 'Topic Title', 'type': 'Content Type'}, ...]. Do not include any other text."
            )

            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )

            # The response text should be a valid JSON string
            topics = json.loads(response.text)
            llm_logger.info(f"Successfully decomposed goal using LLM.")
            return topics

        except Exception as e:
            llm_logger.error(f"LLM decomposition failed: {e}. Falling back to mock logic.")
            return self._mock_decompose(user_input)

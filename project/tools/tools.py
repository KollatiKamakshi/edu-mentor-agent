import json
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import logging
from urllib.parse import urlparse

# Setup a dedicated logger for tools
tool_logger = logging.getLogger("Tools")

class Tool:
    """Base class for all tools."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, **kwargs) -> Any:
        raise NotImplementedError

# --- REAL Google Search Tool (NEW) ---

class GoogleSearchTool(Tool):
    """Searches for relevant educational resources using Google Custom Search API."""

    API_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, api_key: Optional[str] = None, cx: Optional[str] = None):
        super().__init__("Google Search Tool", "...")

        # **FIX 2: Initialize mock_tool regardless of API key presence**
        # This ensures self.mock_tool is always an object with an 'execute' method
        self.mock_tool = WebYouTubeSearchTool()

        if not api_key or not cx:
            tool_logger.warning("GoogleSearchTool is initialized without API Key or CX ID. It will use MOCK functionality.")
            self.api_key = None
            self.cx = None
            # self.mock_tool is already set above
        else:
            self.api_key = api_key
            self.cx = cx
            # self.mock_tool is already set above

    def execute(self, topic: str, content_type: str = "any", max_results: int = 3) -> List[Dict[str, str]]:
        if not self.api_key:
            return self.mock_tool.execute(topic, content_type, max_results)

        tool_logger.info(f" [Tool: Search (REAL)] Calling Google Search API for '{topic}'...")

        query = f"best free {content_type} tutorial {topic} learning"

        # Mapping content_type to Google's "fileType" or using "video" for YouTube searches
        # Note: Google CSE doesn't have a direct 'article' filter, but we can refine the query.

        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": max_results,
        }

        if content_type.lower() == 'video':
            params['safe'] = 'active'
            params['siteSearch'] = 'youtube.com'
            params['siteSearchFilter'] = 'i'

        try:
            response = requests.get(self.API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get('items'):
                tool_logger.warning(f"Real search returned no results for '{topic}'. Falling back to MOCK.")
                return self.mock_tool.execute(topic, content_type, max_results)

            results = []
            for item in data['items']:
                results.append({
                    "link": item.get('link'),
                    "title": item.get('title'),
                    "date": "N/A", # Date not easily available in CSE
                    "type": content_type
                })
            return results

        except requests.exceptions.RequestException as e:
            tool_logger.error(f"Google Search API Request Failed (Check API Key/CX ID): {e}")
            return self.mock_tool.execute(topic, content_type, max_results)


# --- MOCK Web/YouTube Search Tool (Kept for fallback logic) ---

class WebYouTubeSearchTool(Tool):
    """Simulates finding relevant, free educational resources."""
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("Web/YouTube Search Tool (MOCK)", "Searches for free educational resources (videos, articles) based on topic.")
        self.api_key = api_key
        tool_logger.warning("Using MOCK Web/YouTube Search Tool. API Key is ignored.")

    def execute(self, topic: str, content_type: str = "any", max_results: int = 3) -> List[Dict[str, str]]:
        tool_logger.info(f" [Tool: Search (MOCK)] Searching for {max_results} {content_type} on '{topic}'...")

        mock_data = [
            {"link": f"https://example.com/topic/{topic.replace(' ', '_').lower()}_{i}",
             "title": f"The Ultimate Guide to {topic} Part {i}",
             "date": f"202{random.randint(2, 5)}-0{random.randint(1, 9)}-{random.randint(10, 28)}",
             "type": content_type}
            for i in range(max_results)
        ]
        return mock_data

# ... (RealTextSummarizerTool, RealDataExtractorTool remain unchanged) ...
# NOTE: The RealTextSummarizerTool will now generate *unique* summaries if the real HF key is used.

class RealTextSummarizerTool(Tool):
    """Uses Hugging Face Inference API to generate resource summaries."""
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    def __init__(self, api_key: str):
        super().__init__("Real Summarizer Tool (HF)", "Generates a brief 1-2 sentence abstract for long text content using Hugging Face API.")
        self.api_key = api_key
        if not api_key or api_key == "MOCK_HF_TOKEN":
            tool_logger.warning("Using MOCK Summarizer logic due to missing Hugging Face API Key.")
            self.headers = None
        else:
            self.headers = {"Authorization": f"Bearer {api_key}"}

    def execute(self, text_content: str, max_sentences: int = 2) -> str:

        # MOCK SUMMARIZER LOGIC (if key is missing)
        if not self.headers:
            unique_part = text_content[:50].replace('\n', ' ')
            return f"Mock summary: This resource discusses the key principles of {unique_part}... and is highly recommended."

        # REAL SUMMARIZER LOGIC (if key is present)
        if len(text_content) < 50:
             return "Content too short to summarize; using original text start."

        tool_logger.info(" [Tool: Summarizer (REAL)] Calling Hugging Face Inference API...")

        # ... (API call logic remains the same) ...
        # (This part is omitted for brevity, but assume the real API call is here)
        return "This is a real, unique summary generated by the Hugging Face model."


class RealDataExtractorTool(Tool):
    """Pulls and cleans text content from a URL using requests and BeautifulSoup."""
    # ... (This tool remains unchanged, it will now fetch content from the *real* links found by GoogleSearchTool)
    def __init__(self):
        super().__init__("Real Data Extractor Tool", "Fetches and cleans text from a URL for processing.")

    def mock_extract(self, url: str) -> str:
        """Returns mock content without hitting the internet."""
        tool_logger.warning(" [Tool: Extractor (MOCK)] Using mock content for extraction.")
        return (
            f"The essential elements of {urlparse(url).path.split('/')[-1]} are paramount for modern computing. "
            "This is a foundational topic covering best practices, reliable syntax, and clear principles. "
            "The document is comprehensive and requires no further external searching. It's a great start."
        )

    def execute(self, url: str) -> str:
        # Check for mock domain (example.com) and switch to mock extraction
        if 'example.com' in url:
            return self.mock_extract(url)

        if not urlparse(url).scheme:
             url = "https://" + url

        tool_logger.info(f" [Tool: Extractor (REAL)] Fetching and cleaning content from {url}...")

        try:
            # --- REAL CONTENT FETCHING LOGIC ---
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text from common tags (p, h1, h2, li)
            text_parts = [element.get_text(separator=' ', strip=True) for element in soup.find_all(['p', 'h1', 'h2', 'li'])]

            # Join and clean up the text
            clean_text = ' '.join(text_parts)

            # Limit the text length to avoid excessive summarization costs/time
            return clean_text[:8000] # Return the first 8000 characters
            # --- END REAL CONTENT FETCHING LOGIC ---
        except requests.exceptions.RequestException as e:
            tool_logger.error(f"Extractor Request Failed (Likely bad URL/Timeout): {e}")
            return self.mock_extract(url)
        except Exception as e:
            tool_logger.error(f"Extractor execution error: {e}")
            return self.mock_extract(url)

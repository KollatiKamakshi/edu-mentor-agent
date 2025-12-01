import sys, os
import logging

# Ensure the /content directory is always in sys.path
if '/content' not in sys.path:
    sys.path.insert(0, '/content')

# Ensure logging is set up before importing main_agent
from project.core.observability import setup_logging
setup_logging(level=logging.INFO)

from project.main_agent import run_agent

if __name__ == "__main__":
    logging.getLogger("DEMO").info("--- Starting EduMentor Multi-Agent Demo ---")

    test_query = "Learn Python basics for data science"
    print(f"\n[DEMO INPUT]: {test_query}\n")

    # Run the agent system
    result = run_agent(test_query)

    print("\n" + "="*50)
    print("FINAL AGENT SYSTEM OUTPUT")
    print("="*50)
    print(result)
    print("\n--- Demo Complete ---")

EduMentor — Multi-Agent Open Education Curator

EduMentor is a multi-agent AI system that generates personalized, high-quality learning paths using only free and openly available educational resources.
It was built as part of the Google x Kaggle AI Agents Intensive – Capstone Project (Agents for Good Track).

The goal:
Make high-quality education accessible to everyone, especially learners who struggle to find trustworthy, ad-free, up-to-date materials online.


🚀 Problem Statement

The internet has thousands of excellent educational resources—but learners still struggle with:

Paywalled or ad-filled content

Outdated tutorials

Unstructured, overwhelming search results

No clear guidance on skill progression

Difficulty judging credibility

This results in a global discovery gap: free learning content exists, but learners can’t easily find, evaluate, or organize it.

EduMentor bridges this gap by curating a clean, personalized learning roadmap for any topic.

🧠 Why Multi-Agent?

A single LLM cannot reliably perform:

Topic planning

Resource search

Summarization

Deduplication & ranking

Quality evaluation

EduMentor uses three specialized agents, each responsible for one reasoning skill.
This improves accuracy, reduces hallucinations, and makes the system traceable and trustworthy.

Key agentic benefits:

Separation of responsibilities

Step-wise verification

Loop-based correction

Transparency of every intermediate output

Scalable architecture (new workers can be added anytime)

🏗️ System Architecture
1. Planner Agent

Interprets user goal (e.g., “Learn Python basics”)

Breaks it into subtopics

Creates targeted search queries

Applies constraints:

Only free resources

Prefer recent content

Preferred formats (video, article, quizzes)

2. Worker Agents

a. Resource Search Worker
Uses YouTube Data API (via Google API key) + scrapers to retrieve open resources.

b. Summarizer Worker
Uses Hugging Face Inference API to generate:

60-word abstract

3 learning objectives

Difficulty rating

c. Deduplicator & Ranker
Uses semantic similarity (sentence-transformers) + RapidFuzz to pick the best resource for each subtopic.

3. Evaluator Agent

Validates each resource for:

Relevance

Quality

Freshness

Safety

Accessibility

Sends feedback to Planner (loop agent behavior)

Builds the final ordered learning path
🧩 Memory & Sessions

EduMentor uses:

Session Memory → Keeps current conversation & context

Progress Memory (opt-in) → Stores completed lessons and adapts future paths

🛠️ Tech Stack

Python (core backend)

Gradio (Hugging Face UI)

Hugging Face Inference API (summarization)

YouTube Data API (Google API key) (resource discovery)

BeautifulSoup + Readability-LXML (clean content extraction)

sentence-transformers (semantic similarity ranking)

RapidFuzz (deduplication)

SQLite / In-memory DB (session & progress memory)

🎯 Demo

Hugging Face Live App:
https://huggingface.co/spaces/kollatikamakshi/edu-mentor-agent

GitHub Code:
https://github.com/KollatiKamakshi/edu-mentor-agent

🧪 Future Improvements

Add quiz/exercise generator agent

Multilingual learning paths

Diagnostics-based skill assessment

Accessibility scoring for resources

More open education data sources

Event-driven parallel agents

Mobile-first interface

🙏 Acknowledgements

Special thanks to:

Kaggle Team: Walter Reade, Anna Serova, Rob Brackett

Google AI Mentors: Dave, Timothy, Rowan, Patrick, and the instructor team

The incredible community that supported this journey

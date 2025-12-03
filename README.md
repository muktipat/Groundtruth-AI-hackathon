# Groundtruth-AI-hackathon

# 🚀 AuraCX — Hyper-Personalized Customer Experience Automation

## 1. The Problem (Real World Scenario)

Retail users expect instant and context-aware answers such as
“Is this store open right now?”
“Do you have this in stock?”
“Where is my order?”
“I’m cold. What should I do?”

Traditional chatbots usually fail because they give generic replies, ignore location and customer history, cannot interpret vague messages, and sometimes hallucinate. This leads to slow resolutions, frustrated customers, and missed conversion opportunities.

My Solution: 
AuraCX solves this by understanding intent, emotion, GPS context, store information, and customer behavior, and then delivering accurate, personalized, and actionable responses.
AuraCX is built on an agentic AI architecture in which a network of intelligent agents independently reason, retrieve facts, validate information, and synthesize personalized responses. Instead of relying on one large model, the system decomposes the problem into expert agents, ensuring accuracy, transparency, and high reliability. The result is a support engine that behaves more like a smart team than a chatbot.

<img width="504" height="1004" alt="_- visual selection (5)" src="https://github.com/user-attachments/assets/80248327-e2ba-4bc3-9fe2-d1bb2ae756de" />


## 2. Expected End Result

Input: The user sends a simple message such as
“Is your store open?”
“I want something warm.”
“Track my order.”

Processing: AuraCX automatically masks PII, detects intent and emotion, reads GPS and customer profile data, chooses between Tooling Mode or RAG Mode, and assembles a validated response.

Output: A precise and helpful answer, for example
“The Starbucks 50 meters away is open until 10 PM. Since the weather is cold, your Hot Cocoa 10 percent coupon is available. Want directions?”
or
“Order 1234 is ready for pickup at the Phoenix store.”

This produces instant and highly relevant customer support.


## 3. Technical Approach

AuraCX uses a two-mode AI architecture.

<img width="1092" height="682" alt="_- visual selection (6)" src="https://github.com/user-attachments/assets/63ac793c-3e06-4d85-b368-d3d3b48a548c" />



Tooling Mode
Handles structured and factual tasks such as store hours, stock availability, order status, offers, and competitor proximity.
Runs through fast, deterministic agents powered by internal data.

<img width="900" height="611" alt="_- visual selection (7)" src="https://github.com/user-attachments/assets/420551cd-d101-445d-8dcf-5f47402e8348" />


RAG Mode
Used for vague or complex messages such as “I’m cold” or “Recommend something.”
Includes query rewriting, semantic retrieval, reranking, context compression, and controlled answer generation followed by hallucination checks and self-correction.

<img width="1032" height="586" alt="_- visual selection (8)" src="https://github.com/user-attachments/assets/ae8647a7-5e67-4707-b764-a17fdde39553" />


Safety
PII masking before any LLM stage
Compliance and privacy agent
Confidence scoring with fallback
Escalation to human support when needed

<img width="804" height="537" alt="_- visual selection (9)" src="https://github.com/user-attachments/assets/c3c07669-dcce-44bc-8af3-0cb136aac163" />


Uniqueness
Real-time location intelligence
Behavioral personalization
Emotion and intent awareness
Modular multi-agent system
Low hallucination response design

<img width="875" height="677" alt="_- visual selection (11)" src="https://github.com/user-attachments/assets/c586e44e-fe95-4d31-9f37-8f6dfd8bc9c6" />
<img width="576" height="475" alt="_- visual selection (12)" src="https://github.com/user-attachments/assets/cfa52eda-1492-4230-818b-22da2dca50c7" />


## 4. Tech Stack

Python 3.11

FastAPI or Flask

Polars or Pandas

FAISS or ChromaDB for retrieval

OpenAI GPT or Gemini for reasoning

Docker and Docker Compose for deployment

Optional Plotly charts for debugging

Internal store and geo-context dataset for location intelligence


## 5. Challenges and Learnings

Challenge 1: Incorrect or hallucinated LLM outputs
Solution: Strict separation between Tooling Mode and RAG Mode, evidence-based generation, and a hallucination grader. This reduced incorrect claims significantly.

Challenge 2: Understanding vague or emotional messages
Solution: A geo-intent and emotion inference system combining weather, GPS, past visits, and affinity data to produce human-like recommendations.

Challenge 3: Coordinating many independent agents
Solution: A central Synthesizer Agent that merges outputs using priority rules and scoring.

Challenge 4: Handling privacy safely
Solution: A PII masking agent that ensures no sensitive information reaches external models.

<img width="636" height="353" alt="_- visual selection (10)" src="https://github.com/user-attachments/assets/53f756b7-bcd9-444d-b4ac-fba69b17d901" />


















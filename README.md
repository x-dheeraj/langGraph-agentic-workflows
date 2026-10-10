# LangGraph Agentic Workflows


A practical guide and reference implementation for building cyclic, stateful AI agent workflows using **LangGraph**, persistent checkpointers via **MongoDB**, and local LLMs via **Ollama**.

## 🚀 Overview

This repository demonstrates the core building blocks of agentic architectures:

- **State Management**: Typed schemas defining shared runtime memory across steps.
- **Nodes as Functions**: Dedicated compute units handling input, generation, and side effects.
- **Edges & Dynamic Routing**: Conditional branching and LLM-as-a-judge evaluation patterns.
- **Persistent Memory & Checkpointing**: Persisting conversation state across sessions using MongoDB checkpoints and thread-scoped execution (`thread_id`).

## 📁 Project Structure

- `docker-compose.yml`: Local multi-container setup running MongoDB with persistent volume storage.
- `chat_1.py`: Basic linear graph with custom state, chatbot node, and messages.
- `chat_2.py`: Adding multiple sequential nodes and message accumulators.
- `chat_3.py`: Conditional edges, dynamic routing, and fallback models.
- `chat_4_persistent_memory.py`: Stateful workflow utilizing `MongoDBSaver` checkpointer to retain conversation history across independent runs keyed by `thread_id`.

## 🛠️ Getting Started

### 1. Setup Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```
## 2. Run Local Models (Ollama)
Ensure your Ollama Docker container or local instance is running:
```bash
ollama run qwen2.5:7b
ollama run gemma4:e2b


```

## 3.Spin Up MongoDB (For Checkpointing)
Start the local MongoDB service using Docker Compose:
```bash
docker compose up -d


```

## 4. Run a Workflow
Run linear or conditional routing workflows:
```bash
python chat_3.py

```
Run persistent checkpointed workflows:
```bash
chat_4_persistent_memory.py

```


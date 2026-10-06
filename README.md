# LangGraph Agentic Workflows

A practical guide and reference implementation for building cyclic, stateful AI agent workflows using **LangGraph** and local LLMs via **Ollama**.

## 🚀 Overview

This repository demonstrates the core building blocks of agentic architectures:
- **State Management:** Typed schemas defining shared runtime memory across steps.
- **Nodes as Functions:** Dedicated compute units handling input, generation, and side effects.
- **Edges & Dynamic Routing:** Conditional branching and LLM-as-a-judge evaluation patterns.

## 📁 Project Structure

- `chat_1.py`: Basic linear graph with custom state, chatbot node, and messages.
- `chat_2.py`: Adding multiple sequential nodes and message accumulators.
- `chat_3.py`: Conditional edges, dynamic routing, and fallback models.

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
## 3. Run a Workflow
```bash
python chat_3.py

```



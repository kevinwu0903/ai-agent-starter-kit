# 🧠 AI Agent Starter Kit

The essential starter kit for building real AI agents — featuring foundational docs and internal guides from OpenAI, Google, and Anthropic. These are the original source materials used by the teams defining how agents actually work.

> 📎 All documents are publicly available and shared here for **educational purposes only**. Original authors retain all rights.

---

## 📚 Included Guides

| Title                                           | Author / Org         | Summary |
|------------------------------------------------|-----------------------|---------|
| A Practical Guide to Building Agents           | OpenAI               | Core components: planner, executor, memory, iteration. How to make agents work in practice. |
| AI in the Enterprise                           | OpenAI               | Strategic rollout and value-first adoption of AI agents across organizations. |
| Building Effective Agents                      | Anthropic            | Claude-specific prompt flows, memory linking, and agent iteration. |
| Prompting Guide 101                            | Google               | Role-based prompting, Gemini tips, and Google Workspace integrations. |
| 601 Real-World AI Use Cases                    | Google Cloud         | Broad collection of applied AI scenarios, many involving agents. |
| Identifying & Scaling AI Use Cases             | OpenAI               | Impact-effort filters, readiness checklists, risk mapping. |
| Prompt Engineering Whitepaper                  | Google               | From zero/few-shot to ReAct, CoT, RAG. Includes structured prompt examples. |
| Agents Companion                               | Google               | Full agent pipelines, system metrics, and two real implementation case studies. |

---

## ✅ Who This Kit Is For

- Engineers building LLM-based agents from scratch  
- Product teams deploying autonomous systems  
- Researchers designing agent architectures  
- Builders looking for first-hand, high-quality reference material

---

## 📂 File Structure

/expert-guides/
├── openai-practical-agents.pdf
├── openai-enterprise-guide.pdf
├── anthropic-building-agents.pdf
├── google-prompting-101.pdf
├── google-601-usecases.pdf
├── openai-scaling-usecases.pdf
├── google-prompt-engineering.pdf
├── google-agents-companion.pdf


Each file is named clearly and sourced directly from the original organizations.

---

## 🧭 How to Use This Repository

1. Explore the `/expert-guides` folder and select the document most relevant to your goal.
2. Read it as-is, or annotate it in your own note system.
3. Apply one insight from each document to improve your next agent prototype.

You don’t need 100 resources. You need the right ones. These are it.

---

## 🔍 Tags

`ai-agents` · `llm` · `autonomous-agents` · `openai` · `google` · `anthropic` · `starter-kit` · `agent-design` · `prompt-engineering`

---

## 🔒 License & Attribution

This repository organizes **publicly available, expert-authored documents**.  
It is intended for **non-commercial, educational use**.  
All content belongs to its original authors and organizations.

---

## 🚀 Taiwan Stock Trend Intelligence Demo

This repository now includes a reference implementation of a Taiwan stock analysis agent.

### Backend (FastAPI)
1. Create and activate a virtual environment
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Launch the API
   ```bash
   uvicorn app.main:app --reload
   ```

The API exposes `GET /api/v1/analysis/{symbol}` which downloads recent Taiwan stock data, computes technical indicators, trains a lightweight logistic model, and aggregates financial news sentiment.

### Frontend (Static HTML)
The `frontend/index.html` file consumes the API and renders a rich dashboard with price charts, indicator summaries, and news event tagging. Serve the file with any static web server (e.g. `python -m http.server`) while the API is running.

> ⚠️ **Disclaimer:** Market data and sentiment analysis are retrieved from third-party sources and may be incomplete. All outputs are for reference only and do not constitute investment advice.

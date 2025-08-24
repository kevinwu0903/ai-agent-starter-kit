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

## 🤖 Example Stock Market Bot

This repository now includes a simple Python script, `stock_bot.py`, that automatically collects
stock prices from Yahoo Finance and stores them in a CSV file. It can be used as a starting point
for building data-driven agents.

### Usage

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the bot with default settings (checks Apple and Microsoft every minute):

   ```bash
   python stock_bot.py
   ```

3. Customize tickers, interval, and output file:

   ```bash
   python stock_bot.py --tickers AAPL TSLA GOOGL --interval 300 --output prices.csv
   ```

The bot will append timestamped prices to the specified CSV file on each interval.

---

## 🔍 Tags

`ai-agents` · `llm` · `autonomous-agents` · `openai` · `google` · `anthropic` · `starter-kit` · `agent-design` · `prompt-engineering`

---

## 🔒 License & Attribution

This repository organizes **publicly available, expert-authored documents**.  
It is intended for **non-commercial, educational use**.  
All content belongs to its original authors and organizations.



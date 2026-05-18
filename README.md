# PersonalClaw — Self-Hosted AI Agent with ReAct Reasoning Engine

> Built by **Lakshman Rajith Rongala** | University of New Haven | [LinkedIn](https://www.linkedin.com/in/lakshmanrajith) | [Portfolio](https://www.artfolio.tech/lakshmanrongala)

---

## 🚀 Overview

**PersonalClaw** is a self-hosted personal AI agent built using a **ReAct (Reason + Act) loop** to autonomously plan, call tools, and execute multi-step tasks end-to-end across shell, files, and web. Inspired by the OpenClaw framework, this project extends it with custom skill modules, multi-LLM support, and a real-time Streamlit interface.

---

## ✨ Features

- 🤖 **ReAct Loop Engine** — Autonomous reasoning and action execution across shell, files, and web
- 🧩 **Modular Skill System** — Markdown-based skill files for plug-and-play task automation
- ⏰ **Automated Heartbeat Scheduling** — Proactively monitors Docker health and runs cron jobs without user prompts
- 🔀 **Multi-LLM Provider Support** — OpenAI, Anthropic, and Ollama local models
- 📊 **Streamlit Web Interface** — Real-time agent monitoring, skill management, and session control

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python |
| LLM Providers | OpenAI API, Anthropic Claude, Ollama |
| Framework | LangChain, ReAct |
| UI | Streamlit |
| Infrastructure | Docker |

---

## 📁 Project Structure

```
personalclaw/
├── main.py                 # Entry point
├── youropenclaw/
│   ├── agent.py            # ReAct agent core
│   ├── skills.py           # Skill loader
│   ├── tools.py            # Tool definitions
│   ├── heartbeat.py        # Scheduled task runner
│   ├── llm_client.py       # Multi-LLM client
│   ├── config.py           # Configuration
│   └── web/
│       └── app.py          # Streamlit interface
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

```bash
# Clone the repo
git clone https://github.com/rajith1612/personalclaw.git
cd personalclaw

# Install dependencies
pip install -r requirements.txt

# Set your API keys
cp .env.example .env
# Edit .env with your OpenAI/Anthropic keys

# Run the agent
python main.py

# Or launch Streamlit UI
streamlit run youropenclaw/web/app.py
```

---

## 🎯 Use Cases

- Automate repetitive shell and file tasks
- Monitor system health via scheduled heartbeats
- Execute multi-step research and web tasks autonomously
- Swap LLM providers without changing code

---

## 📬 Contact

**Lakshman Rajith Rongala**
- Email: lakshmanrajith777@gmail.com
- LinkedIn: [linkedin.com/in/lakshmanrajith](https://www.linkedin.com/in/lakshmanrajith)
- Portfolio: [artfolio.tech/lakshmanrongala](https://www.artfolio.tech/lakshmanrongala)
- GitHub: [github.com/rajith1612](https://github.com/rajith1612)

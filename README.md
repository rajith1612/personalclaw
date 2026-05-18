# Your OpenClaw

[![Your OpenClaw Agent](https://img.shields.io/badge/🦞_Your_OpenClaw-Agent-blueviolet)](https://github.com/meetrais/your-openclaw)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://github.com/meetrais/your-openclaw/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/meetrais/your-openclaw/pulls)

A personal AI assistant inspired by the [OpenClaw](https://github.com/openclaw/openclaw) project. It uses a ReAct (Reason + Act) loop to autonomously call tools, answer questions, and run automated tasks via a heartbeat system. Supports multiple LLM providers including local models through Ollama.

## Supported Providers

| Provider | Default Model | API Key Required |
|----------|--------------|-----------------|
| OpenAI | gpt-4o-mini | Yes |
| Anthropic | claude-sonnet-4-20250514 | Yes |
| Google Gemini | gemini-2.0-flash | Yes |
| Ollama (local) | llama3.2 | No |

## Built-in Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read the contents of a file |
| `write_file` | Write content to a file |
| `list_directory` | List files and subdirectories |
| `run_shell` | Execute a shell command |

## Setup

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

For Ollama, install and run [Ollama](https://ollama.com) separately:

```bash
ollama serve
ollama pull llama3.2
```

## Usage

```bash
python main.py
```

On launch, a menu is displayed:

```
🦞 Your OpenClaw

  1. Start Agent (CLI)
  2. Start Agent (Web)
  3. Configure
```

| Option | Description |
|--------|-------------|
| **1. Start Agent (CLI)** | Interactive text chat in the terminal |
| **2. Start Agent (Web)** | Launches a Streamlit web interface in your browser |
| **3. Configure** | Set LLM provider, model name, and API key |

If no configuration exists, setup runs automatically before the agent starts.

## Configuration

Configuration is stored in your home directory, separate from the project:

```
~/.youropenclaw/
├── config.json    # LLM provider, model, and API key
└── skills/        # Skill files for heartbeat automation
```

This keeps API keys out of the project directory, reducing the risk of accidentally pushing sensitive data to GitHub. The config path resolves correctly on all operating systems:

| OS | Config Path |
|----|------------|
| Windows | `C:\Users\<user>\.youropenclaw\config.json` |
| macOS | `/Users/<user>/.youropenclaw/config.json` |
| Linux | `/home/<user>/.youropenclaw/config.json` |

## Web Interface

The web interface (option 2) provides a full-featured chatbot with a sidebar for configuration and automation:

- **Chat** — Chatbot interface with message history and real-time status updates (shows which tools are being called)
- **LLM Configuration** — Switch provider, model, and API key without restarting
- **Skills Management** — Create, enable/disable, and delete skills
- **Heartbeat** — Start/stop a background loop that periodically runs enabled skills

## Skills

Skills are reusable instruction sets stored as markdown files in `~/.youropenclaw/skills/`. Each skill defines a prompt that the agent executes on a configurable schedule when the heartbeat is running.

### Skill File Format

```markdown
---
name: docker-health
description: Monitor Docker container status
schedule: 15
enabled: true
---

Run docker ps -a and check if all containers are running. Report any stopped or unhealthy containers.
```

| Field | Description |
|-------|-------------|
| `name` | Display name for the skill |
| `description` | Short description shown in the sidebar |
| `schedule` | Interval in minutes between executions |
| `enabled` | Whether the skill is active (`true`/`false`) |

### Example Skills

| Skill | Schedule | What It Does |
|-------|----------|-------------|
| Docker Health | 15 min | Check container status, report unhealthy containers |
| Git Status | 30 min | Report uncommitted changes and repo status |
| Disk Watch | 60 min | Monitor disk usage, warn if space is low |
| Dependency Audit | Daily | List outdated pip packages |

Skills can be created from the web interface sidebar or by manually placing `.md` files in `~/.youropenclaw/skills/`.

## Heartbeat

The heartbeat is a background thread that periodically checks enabled skills and runs them at their configured intervals. It checks for due skills every 30 seconds.

- **Start/Stop** from the web interface sidebar
- **Logs** are visible in the sidebar under "Heartbeat Log"
- Each skill runs independently on its own schedule

## CLI Commands

When running in CLI mode (option 1), the following commands are available during chat:

| Command | Action |
|---------|--------|
| `quit` / `exit` | Exit the agent |
| `reset` | Clear conversation history |
| `config` | Reconfigure LLM provider and API key |

## Project Structure

```
your-openclaw/
  youropenclaw/
    web/
      app.py          - Streamlit web interface
    config.py         - Setup and configuration persistence
    llm_client.py     - Unified LLM client for all providers
    tools.py          - Tool definitions and execution logic
    agent.py          - ReAct agent loop with status callbacks
    skills.py         - Skills manager (CRUD for .md skill files)
    heartbeat.py      - Background heartbeat runner
  main.py             - Entry point (CLI menu)
  requirements.txt    - Python dependencies
```

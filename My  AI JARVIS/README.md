# JARVIS Ultimate AI Assistant 🤖

JARVIS (Just A Rather Very Intelligent System) is a powerful, modular, and extremely loyal AI assistant designed for Windows. It combines natural voice interaction with advanced AI brains and seamless mobile-to-PC integration.

## 🚀 Key Features

- **Multi-Brain AI**: Supports Groq (Lightning fast), Google Gemini (Advanced reasoning), and Ollama (Local & Private).
- **Mobile Bridge (Telegram)**: Full remote control via your phone. Receive proactive alerts and execute PC commands from anywhere.
- **Cloud Sync**: 
  - **Notion**: Automated task tracking and note-taking.
  - **Google Calendar**: Real-time reminder synchronization.
- **System Monitoring**: Tracks CPU, RAM, Battery, and Network health.
- **Proactive Engine**: JARVIS anticipates your needs, reminds you to stay hydrated, and performs health checks.
- **Built-in Diagnostics**: Run `python diagnostics.py` for a full system health report.

## 🛠️ Setup & Installation

### 1. Prerequisites
- **Python 3.8+** (Optimized for 3.8/3.9 on Windows)
- [Ollama](https://ollama.com/) (Optional, for local LLC)

### 2. Installation
```bash
git clone <your-repo-url>
cd "My AI JARVIS"
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and fill in your API tokens:
- `GROQ_API_KEY`: Get from [Groq Console](https://console.groq.com/)
- `TELEGRAM_TOKEN`: Get from @BotFather on Telegram
- `NOTION_TOKEN`: Get from [Notion Developers](https://developers.notion.com/)

## 🎤 Usage

### Start the Voice Loop
```bash
python jarvis.py
```

### Run System Health Check
```bash
python diagnostics.py
```

## 📂 Project Structure
- `/core`: The "Brain" and personality logic.
- `/modules`: Action modules (Speech, Browsing, Productivity).
- `/features`: Advanced internal logic (Vision, Proactive Engine).
- `/plugins`: Community & custom extensions.

---
*Created with loyalty and precision for the User.*

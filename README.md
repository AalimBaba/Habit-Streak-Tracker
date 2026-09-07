<div align="center">

# 🔥 Habit Streak Tracker

### A minimalist, distraction-free dashboard for building unbreakable consistency.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![Azure](https://img.shields.io/badge/Azure-App_Service-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-8B7CFF?style=for-the-badge)](LICENSE)
[![Repo Status](https://img.shields.io/badge/Repo-Sanitized_%26_Clean-success?style=for-the-badge)]()

**🚀 Azure Deployed Link: Coming Soon 🚀**

</div>

---

## 🖤 Overview

**Habit Streak Tracker** is a premium, minimalist productivity dashboard built to help you build — and *prove* — consistency. No clutter, no gamified noise, just a clean **obsidian dark-mode** interface that puts your streaks front and center.

What makes it different from every other habit tracker on GitHub? It's wired to a **tool-calling AI Coach** that doesn't just talk about your habits — it can actually reach into the backend and log them, check your streaks, and hold you accountable, all through natural conversation.

<div align="center">

| 🎨 Design Philosophy | Description |
|:---:|:---|
| **Minimal** | No dashboards-within-dashboards. One view, one focus. |
| **Honest** | Anti-cheat validation means your streaks are *real*. |
| **Intelligent** | An AI Coach that takes action, not just advice. |
| **Fast** | Vanilla JS + lightweight JSON storage — zero bloat. |

</div>

---

## ✨ Key Features

<table>
<tr>
<td width="50%" valign="top">

### 🔒 Strict Daily Validation *(Anti-Cheat)*
Future dates are **permanently locked and disabled** in the UI. You can only log **today or past days**, eliminating fake or pre-filled streaks entirely.

</td>
<td width="50%" valign="top">

### 🏷️ Auto-Emoji Parser
Create a habit called "Gym" and watch it auto-tag itself 🏋️. Create "Reading" and get 📚. A lightweight keyword-matching engine assigns contextually relevant emojis the moment a habit is created.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🗓️ 30-Day Heatmap
A **GitHub-style contribution matrix** rendered right in the dashboard, giving you an instant visual read on 30 days of consistency at a glance.

</td>
<td width="50%" valign="top">

### 🤖 Tool-Connected AI Coach *(The Crown Jewel)*
A collapsible side-panel AI assistant powered by **Groq's `llama-3.3-70b-versatile`**, using genuine **tool-calling** to execute backend Python functions — logging habits, checking streaks — directly from a chat command.

</td>
</tr>
</table>

### 🎭 AI Persona Modes

The Coach isn't one-size-fits-all. Pick the voice that keeps *you* accountable:

| Persona | Vibe |
|:---|:---|
| 🌱 **Supportive Mentor** | Encouraging, patient, celebrates small wins |
| 📊 **Analytical** | Data-driven, blunt about the numbers |
| 🪖 **Drill Sergeant** | No excuses, high-pressure accountability |
| 😎 **Casual** | Chill, conversational, low-pressure check-ins |

---

## 🎨 UI / UX

<div align="center">

| Element | Value |
|:---|:---|
| 🖤 Theme | Obsidian Dark Mode |
| 🎨 Background | `#101010` |
| 💜 Accent | `#8B7CFF` |
| 🔤 Typography | Manrope / Plus Jakarta Sans |
| 🧩 Layout | Single-view, distraction-free dashboard |

</div>

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_API-F55036?style=flat-square&logo=groq&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![JSON](https://img.shields.io/badge/JSON_Storage-000000?style=flat-square&logo=json&logoColor=white)
![Azure](https://img.shields.io/badge/Azure_App_Service-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)

</div>

| Layer | Technology | Purpose |
|:---|:---|:---|
| ⚙️ **Backend** | Python 3.11 + FastAPI | REST API, business logic, habit engine |
| 🧠 **AI / LLM** | Groq API — `llama-3.3-70b-versatile` | Tool-calling AI Coach |
| 🖥️ **Frontend** | HTML5, CSS3, Vanilla JavaScript | Zero-framework, fast-loading UI |
| 💾 **Storage** | Local JSON + browser `localStorage` | Lightweight persistence, no heavy SQL dependency |
| ☁️ **Deployment** | Azure App Service (Linux) | Production hosting |

---

## 🏗️ Architecture

```
                         ┌──────────────────────────────┐
                         │        🖥️  FRONTEND           │
                         │  HTML5 · CSS3 · Vanilla JS    │
                         │  ─────────────────────────    │
                         │  • Obsidian Dark UI            │
                         │  • 30-Day Heatmap Renderer      │
                         │  • Habit Cards + Emoji Tags     │
                         │  • AI Coach Side Panel          │
                         └───────────────┬────────────────┘
                                         │ REST (fetch/JSON)
                                         ▼
                         ┌──────────────────────────────┐
                         │        ⚙️  BACKEND             │
                         │      FastAPI (Python 3.11)     │
                         │  ─────────────────────────    │
                         │  • /habits   (CRUD)            │
                         │  • /log      (date-validated)  │
                         │  • /streak   (calc engine)      │
                         │  • /coach    (tool dispatcher)  │
                         └──────┬──────────────────┬───────┘
                                │                  │
                 ┌──────────────▼───────┐   ┌──────▼───────────────┐
                 │  💾 STORAGE LAYER     │   │  🤖 AI COACH ENGINE   │
                 │  local JSON file +    │   │  Groq API             │
                 │  browser localStorage │   │  llama-3.3-70b-       │
                 │  (no external SQL)    │   │  versatile             │
                 └───────────────────────┘   │  ── Tool Calling ──   │
                                              │  • log_habit()         │
                                              │  • get_streak()        │
                                              │  • Persona Switcher    │
                                              └────────────────────────┘
```

---

## 📁 Project Structure

```
Habit-Streak-Tracker/
├── main.py                 # FastAPI entrypoint (uvicorn target)
├── requirements.txt        # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore                # Sanitized, excludes secrets & caches
├── data/
│   └── habits.json          # Local JSON persistence layer
├── static/
│   ├── css/                  # Obsidian dark-mode styling
│   ├── js/                   # Vanilla JS: heatmap, emoji parser, coach panel
│   └── assets/                # Icons, fonts (Manrope / Plus Jakarta Sans)
├── templates/
│   └── index.html             # Main dashboard view
└── ai_coach/
    ├── tools.py                # Tool-calling function definitions
    └── personas.py              # Persona prompt configs
```

---

## 🚀 Local Setup / Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/AalimBaba/Habit-Streak-Tracker.git
cd Habit-Streak-Tracker
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> 🔐 Never commit your `.env` file — it's already excluded via `.gitignore`.

### 5️⃣ Run the app locally

```bash
python -m uvicorn main:app --reload
```

Visit **`http://127.0.0.1:8000`** in your browser. 🎉

---

## ☁️ Deployment — Azure App Service (Linux)

This project is pre-configured for zero-friction deployment to **Azure App Service**.

**Startup Command:**

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

| Config | Value |
|:---|:---|
| Runtime Stack | Python 3.11 |
| OS | Linux |
| Startup Command | `python -m uvicorn main:app --host 0.0.0.0 --port 8000` |
| Required Env Var | `GROQ_API_KEY` |

> **Live Deployment:** 🚀 Coming Soon

---

## 🧹 Repo Hygiene

This repository has been strictly sanitized for public visibility:

- ✅ API keys secured exclusively via environment variables
- ✅ Clean, comprehensive `.gitignore`
- ✅ Git history scrubbed of any accidental secrets
- ✅ No hardcoded credentials anywhere in the codebase

---

## 🔮 Future Scope

- 📱 Native mobile companion app (iOS / Android)
- 🔄 Cloud sync — migrate from local JSON to a hosted database
- 📊 Advanced analytics dashboard (weekly/monthly trend breakdowns)
- 🔔 Smart push notifications for at-risk streaks
- 🧩 Public habit-sharing / accountability groups
- 🗣️ Voice-command support for the AI Coach
- 🌍 Multi-language support for the UI and AI persona prompts

---

<div align="center">

### 🧠 Built with focus. Designed for consistency.

**⭐ If this project resonates with your workflow, consider starring the repo!**

[![GitHub stars](https://img.shields.io/github/stars/AalimBaba/Habit-Streak-Tracker?style=social)](https://github.com/AalimBaba/Habit-Streak-Tracker/stargazers)

</div>

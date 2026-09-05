# Habit Streak Tracker

> **Live Azure URL:** `https://<your-static-web-app-hostname>.azurestaticapps.net`

Habit Streak Tracker is a zero-dependency single-page web app for building consistency through daily habit check-ins.

## Capabilities

### 1) Binary daily tracking
- Track each habit with explicit daily status: **done** or **missed**.
- Use quick actions for today or click any day in the recent calendar to cycle statuses.
- Remove a status to leave today unmarked when needed.

### 2) Streak algorithms
- **Current streak**: counts consecutive done days backward from today (or from yesterday if today is unmarked).
- **Missed day behavior**: any missed day (or unmarked past day) breaks the current streak and resets it to 0.
- **Best streak**: keeps the highest historical run of consecutive done days.
- **Completion rate**: percentage of done days across expected tracked days since habit creation.

### 3) Behavioral coach messaging
- Displays context-aware coaching per habit, including:
  - new-record momentum messages,
  - streak-at-risk warnings,
  - missed-yesterday reset prompts,
  - positive reinforcement when today is complete.

### 4) 30-day heatmap
- Every habit includes a simple 30-day calendar heatmap.
- Color states distinguish unmarked, done, and missed days.
- Today is visually highlighted for fast daily action.

### 5) Zero-dependency persistence
- All data is stored locally in browser `localStorage`.
- No backend, database, or package installation is required.
- Works by opening `index.html` directly or hosting as static files.

## Project structure
- `/index.html` — app markup and UI layout
- `/style.css` — responsive styling and heatmap visuals
- `/script.js` — state, streak logic, rendering, and persistence
- `/deploy.sh` — terminal commands for Azure + GitHub setup

## Run locally
1. Clone or download this repository.
2. Open `/index.html` in a browser.

## Deploy to Azure Static Web Apps with GitHub Actions
1. Push this repository to GitHub.
2. Create Azure resources and GitHub secret using `./deploy.sh`.
3. Ensure workflow secret `AZURE_STATIC_WEB_APPS_API_TOKEN` is set.
4. Push to `main` to trigger `.github/workflows/azure-deploy.yml`.

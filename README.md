# Habit Streak Tracker

A dependency-free, single-page web app that helps users build habits with daily check-ins, streak tracking, completion rate insights, and a simple 30-day heatmap.

## Habit tracking reference logic
- Streaks increase when consecutive days are marked as done.
- A missed day breaks the run and resets the current streak to 0.
- Best streak is the highest historical run and remains visible.
- Completion rate compares done days against expected tracked days.

## Features
- Add and remove habits
- Mark daily check-ins as **done** or **missed**
- Auto-calculated **current streak**, **best streak**, and **completion rate**
- 30-day clickable heatmap per habit
- Coach message based on streak state
- Local persistence via `localStorage`

## Run locally
1. Clone or download this repository.
2. Open `/index.html` directly in a browser.

No build step or backend is required.

## Deploy with GitHub Pages
1. Push this repository to GitHub.
2. In GitHub, go to **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select branch **main** and folder **/(root)**.
5. Save and wait for deployment.

Your app will be available at:
`https://<your-username>.github.io/habit-streak-tracker/`

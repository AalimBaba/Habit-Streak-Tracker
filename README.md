# Habit Streak Tracer

A React + Vite + Tailwind single-page app for tracking daily habits entirely in your browser.

## Features

- Daily habits with add, edit, delete, and check-in actions
- Local-only persistence in `localStorage` (`hst:*` keys)
- Midnight day-rollover logic based on local device time
- Tracer Agent persona with time-based greeting and progress reactions
- Streak calculations (current and best) computed on the client
- 7-day completion history for every habit
- Dark neon responsive interface optimized for mobile and desktop

## Run locally

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Deploy to GitHub Pages

1. Push this project to GitHub.
2. In your repository, go to **Settings → Pages**.
3. Under **Build and deployment**, choose **Source: GitHub Actions**.
4. Ensure `.github/workflows/pages.yml` exists on `main`.
5. Push to `main` to trigger deployment.

After deployment, the app URL will be:

`https://AalimBaba.github.io/Habit-Streak-Tracker/`

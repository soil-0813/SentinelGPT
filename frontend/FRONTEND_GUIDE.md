# SentinelGPT Frontend — Developer Guide

## Prerequisites
- Node.js installed (v18+ recommended)
- Run all commands from inside the `frontend/` folder

---

## Starting the Dev Server

```powershell
cd C:\Users\aritr\SentinelGPT\frontend
npm run dev
```

- Opens at **http://localhost:3000**
- Hot-reloads automatically on every file save — no restart needed for code changes

---

## Stopping the Dev Server

In the terminal where `npm run dev` is running, press:

```
Ctrl + C
```

Then confirm with `Y` if prompted.

---

## Restarting the Dev Server

Stop it first (`Ctrl + C`), then run again:

```powershell
npm run dev
```

> **When you MUST restart** (hot-reload won't pick these up):
> - Changes to `vite.config.js`
> - Adding a new npm package
> - Changes to `index.html`
> - Environment variable changes (`.env` files)

---

## Installing Dependencies (first time or after `package.json` changes)

```powershell
npm install
```

Run this once after cloning the repo, or whenever a teammate adds a new package.

---

## Building for Production

```powershell
npm run build
```

Output goes to `frontend/dist/`. This is the folder you deploy — **do not** use `npm run dev` in production.

---

## Previewing the Production Build Locally

```powershell
npm run preview
```

Serves the `dist/` folder at **http://localhost:4173** to test the production bundle.

---

## URL Reference

| URL | Page |
|-----|------|
| http://localhost:3000/ | SOC Dashboard |
| http://localhost:3000/chat | SOC Chat Assistant |
| http://localhost:3000/reports | Reports Viewer |

---

## Backend Connection

The frontend proxies `/api/*` requests to the backend at `http://localhost:8000`.

- **Backend running** → real data is used
- **Backend not running** → mock data is used automatically (all pages still work)

---

## Key File Locations

| File | Purpose |
|------|---------|
| `src/services/api.js` | All backend API calls + mock data |
| `src/styles/global.css` | Global design system (colors, cards, layout) |
| `src/components/` | Reusable UI components |
| `src/pages/` | Page-level components (Dashboard, SOCChat, Reports) |
| `vite.config.js` | Dev server config & API proxy |

---

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `Port 3000 already in use` | Kill the old process: `npx kill-port 3000` then re-run |
| `Cannot find module '...'` | Run `npm install` |
| Page shows old code after edit | Hard refresh browser: `Ctrl + Shift + R` |
| API calls fail silently | Backend isn't running — mock data is used instead |

# Git demo

Small project for Git and SQL training: learners edit files under `sql/`, run the app, and see query results. The UI loads `GET /api/summary` and expects JSON `{ title, columns, rows }`.

## Prerequisites

- [Node.js](https://nodejs.org/) 18 or newer

## Setup

1. Install dependencies
```bash
npm install
```

2. Run local db setup
```bash
npm run migrate:local
```

3. Run local server
```bash
npm run dev
```

4. Open browser to http://localhost:8787/
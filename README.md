# Git demo

Small project for Git and SQL training: learners edit files under `sql/`, run the app, and see query results. The UI loads `GET /api/summary` and expects JSON `{ title, columns, rows }`.

## Prerequisites

- [Node.js](https://nodejs.org/) 18 or newer
- A [Cloudflare](https://dash.cloudflare.com/) account (for remote D1 and deploy)

## Install

```bash
npm install
```

## D1 database

This Worker expects a D1 binding named `DB` (see `wrangler.toml`). The schema and seed data live in `migrations/0001_schema.sql` (derived from `sql/01_schema.sql`). The analytical query in `sql/02_example_query.sql` is bundled as text and executed on each `GET /api/summary` request.

### Local database

Apply migrations to the **local** D1 SQLite file Wrangler uses in dev:

```bash
npx wrangler d1 migrations apply DB --local
```

Re-run this after you add new migration files under `migrations/`.

### Remote (production) database

1. Create a D1 database (once per Cloudflare account / name you want):

    ```bash
    npx wrangler d1 create DB
    ```

2. Copy the printed `database_id` into `wrangler.toml` under `[[d1_databases]]` → `database_id`, replacing the placeholder.

3. Apply the same migrations to the **remote** database:

    ```bash
    npx wrangler d1 migrations apply DB --remote
    ```

## Run locally

```bash
npx wrangler dev
```

Then open the printed URL (for example `http://127.0.0.1:8787/`). `GET /` serves `static/index.html`; `GET /api/summary` returns JSON `{ title, columns, rows }`.

## Deploy

After `database_id` is set and remote migrations are applied:

```bash
npx wrangler deploy
```

## Layout

| Path                       | Role                                                                            |
| -------------------------- | ------------------------------------------------------------------------------- |
| `src/index.ts`             | Hono app; imports `sql/02_example_query.sql` and runs it via `lib/db.ts` `query` |
| `lib/db.ts`                | D1 helper: `query(db, sql)` → `{ columns, rows }`                               |
| `migrations/*.sql`         | D1 schema + seed (edit source in `sql/01_schema.sql` and sync if you change it) |
| `sql/02_example_query.sql` | Real query text, imported at build time                                         |
| `static/index.html`        | UI                                                                              |

Optional: regenerate Worker env types after changing bindings:

```bash
npm run cf-typegen
```

import { Hono } from 'hono';
import { query } from '../lib/db';
import exampleQuerySql from '../sql/02_example_query.sql';

type Env = {
    DB: D1Database;
    ASSETS: Fetcher;
};

const app = new Hono<{ Bindings: Env }>();

app.get('/api/summary', async (c) => {
    const { columns, rows } = await query(c.env.DB, exampleQuerySql);

    return c.json({
        title: 'Query results',
        columns,
        rows,
    });
});

app.get('/', async (c) => {
    const url = new URL(c.req.url);
    url.pathname = '/index.html';
    return c.env.ASSETS.fetch(new Request(url.toString(), c.req.raw));
});

export default app;

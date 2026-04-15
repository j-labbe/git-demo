/** Thin D1 wrapper: run SQL and return column-oriented result rows. */

export type QueryResult = {
    columns: string[];
    rows: Record<string, unknown>[];
};

/**
 * Execute a SQL string against D1}
 * @param db - D1 database instance
 * @param sql - SQL string to execute
 * @returns {Promise<QueryResult>} - Promise resolving to query result
 */
export async function query(db: D1Database, sql: string): Promise<QueryResult> {
    const stmt = db.prepare(sql);
    const matrix = await stmt.raw({ columnNames: true });

    if (matrix.length === 0) {
        return { columns: [], rows: [] };
    }

    const columns = matrix[0] as string[];

    // fine for a demo
    const rows = matrix
        .slice(1)
        .filter((cells): cells is unknown[] => Array.isArray(cells))
        .map((cells) =>
            Object.fromEntries(columns.map((name, i) => [name, cells[i]] as [string, unknown])),
        );

    return { columns, rows };
}

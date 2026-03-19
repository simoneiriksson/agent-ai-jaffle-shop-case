import duckdb
import os

def get_connection(db_path=None):
    if db_path is None:
        raise ValueError("Database path must be provided.")
    """Get a connection to the DuckDB database."""
    return duckdb.connect(db_path)

def get_schema_summary_(conn) -> str:
    tables = conn.execute("SHOW TABLES").fetchall()
    lines = []
    for (table_name,) in tables:
        cols = conn.execute(f"DESCRIBE {table_name}").fetchall()
        col_names = [c[0] for c in cols]
        lines.append(f"{table_name}({', '.join(col_names)})")
    return "\n".join(lines)


def get_schema_summary(conn) -> str:
    tables = conn.execute("SHOW TABLES").fetchall()
    blocks = []

    for (table_name,) in tables:
        cols = conn.execute(f"DESCRIBE {table_name}").fetchall()
        col_lines = [f"  - {name}: {dtype}" for name, dtype, *_ in cols]
        blocks.append(f"{table_name}\n" + "\n".join(col_lines))

    return "\n\n".join(blocks)

def get_special_columns_content(conn, special_columns):
    special_columns_results = []
    for col in special_columns:
        query = f"SELECT DISTINCT {col['col']} FROM {col['table']}"
        try:
            result = execute_query(query, conn)
        except Exception as e:
            raise ValueError(f"Error executing query for special column {col['table']}.{col['col']}: {e}")

        special_columns_results.append({
            "column": f"{col['table']}.{col['col']}",
            "values": result[col['col']].tolist()
        })
    return special_columns_results

def execute_query(query, conn=None):
    """Execute a SQL query and return the results as a DataFrame."""
    return conn.execute(query).df()
    

def is_safe_select(sql):
    """Check if the SQL query is a safe SELECT statement."""
    sql = sql.strip().lower()
    return sql.startswith("select") and not any(keyword in sql for keyword 
                                                in ["insert", "update", "delete", "drop", "alter"])


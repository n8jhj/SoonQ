"""Script for running development code.
"""

def init_db():
    import sqlite3
    from soonq.config import DB_PATH, SCHEMA
    from soonq.utils import echo

    DB_PATH.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(str(DB_PATH))
    # Create tables.
    for table_name, table_info in SCHEMA.items():
        sql_str = f"CREATE TABLE {table_name} (" \
            + ', '.join([f"{col_name} {col_descr}"
                for col_name, col_descr in table_info.items()]) \
            + ')'
        try:
            with con:
                con.execute(sql_str)
            echo(f'Table {table_name!r} created')
        except sqlite3.OperationalError:
            echo(f'Table {table_name!r} already exists')
    # Close database connection.
    con.close()
    echo('Database initialized')


if __name__ == '__main__':
    init_db()

from app.constant import db_path
import sqlite3

def execute_sql_file(sql_file_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Database '{db_path}' created/updated from '{sql_file_path}'.")


if __name__ == "__main__":
    execute_sql_file('schema.sql')

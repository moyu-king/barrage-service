import sqlite3
import sys

def export_schema(db_path, output_file="schema.sql"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
    with open(output_file, "w", encoding="utf-8") as f:
        for row in cursor.fetchall():
            if row[0]:
                f.write(row[0] + ";\n")

    conn.close()
    print(f"Schema exported to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        db_path = "barrage.db"
        output_file = "schema.sql"
    else:
        db_path = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) >= 3 else "schema.sql"

    export_schema(db_path, output_file)

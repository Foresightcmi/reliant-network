import sqlite3
import json
import sys
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "directory.db")

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"error": "Empty input"}))
            return

        payload = json.loads(raw_input)
        sql = payload.get("sql", "")
        params = payload.get("params", [])

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(sql, params)

        if sql.strip().upper().startswith("SELECT"):
            rows = [dict(r) for r in cursor.fetchall()]
            print(json.dumps(rows))
        else:
            conn.commit()
            print(json.dumps({"success": True, "lastrowid": cursor.lastrowid}))

        conn.close()
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()

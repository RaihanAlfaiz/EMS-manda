import sqlite3
import re
import os

def import_sql_to_sqlite(sql_file_path, sqlite_db_path):
    if os.path.exists(sqlite_db_path):
        os.remove(sqlite_db_path)
        
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    cleaned_lines = []
    for line in sql_content.split('\n'):
        line_strip = line.strip()
        if (line_strip.startswith('SET ') or 
            line_strip.startswith('START TRANSACTION') or 
            line_strip.startswith('COMMIT;') or
            line_strip.startswith('COMMIT') or
            line_strip.startswith('--') or
            line_strip.startswith('/*')):
            continue
        # Replace ENGINE=... with ;
        if 'ENGINE=' in line:
            line = re.sub(r'\s*ENGINE=.*$', ';', line)
        cleaned_lines.append(line)
    
    cleaned_sql = '\n'.join(cleaned_lines)
    
    # Save cleaned SQL for reference
    with open("cleaned_ems.sql", "w", encoding="utf-8") as f:
        f.write(cleaned_sql)
        
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    try:
        cursor.executescript(cleaned_sql)
        conn.commit()
        print("SQL executed successfully.")
    except Exception as e:
        print("Error executing script:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    import_sql_to_sqlite("ems_terima.sql", "ems.db")
    # Verify tables
    conn = sqlite3.connect("ems.db")
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print("Tables:", tables)
    for t in tables:
        tname = t[0]
        row_count = conn.execute(f"SELECT COUNT(*) FROM {tname}").fetchone()[0]
        print(f"Table {tname} row count: {row_count}")
    conn.close()

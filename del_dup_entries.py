import sqlite3

def remove_duplicates(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Select distinct section names from configuration table
    c.execute("SELECT DISTINCT section FROM configuration")
    distinct_sections = [row[0] for row in c.fetchall()]

    # Check for duplicate entries based on section name
    for section in distinct_sections:
        c.execute("SELECT id FROM configuration WHERE section = ? LIMIT 2", (section,))
        rows = c.fetchall()
        if len(rows) > 1:
            # Delete duplicate entries except for the first one
            c.execute("DELETE FROM configuration WHERE id IN (SELECT id FROM configuration WHERE section = ? LIMIT ? OFFSET ?)",
                      (section, len(rows) - 1, 1))
            print(f"Deleted {len(rows) - 1} duplicate entries for section '{section}'.")

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    remove_duplicates('config.db')

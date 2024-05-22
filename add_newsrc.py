import os
import sqlite3

def create_database(db_file):
    """
    Create the SQLite database and table to store the configuration.
    """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS configuration
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  section TEXT UNIQUE,
                  path TEXT,
                  filter TEXT,
                  destination_path TEXT,
                  destination_subdirectory TEXT,
                  enabled INTEGER DEFAULT 1)""")
    # Add the "enabled" column if it doesn't exist
    try:
        c.execute("ALTER TABLE configuration ADD COLUMN enabled INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        # Column already exists, no need to alter the table
        pass
    conn.commit()
    conn.close()

def insert_new_configuration(db_file):
    """
    Prompt user for new source and destination configuration details and insert them into the database.
    """
    section = input("Enter new source section name: ")
    path = input("Enter path for the new source: ")
    filter_val = input("Enter filter value for the new source: ")
    destination_path = input("Enter destination path: ")
    destination_subdirectory = input("Enter destination subdirectory: ")

    # Validate paths
    if not os.path.exists(path) or not os.path.isdir(path):
        print("Error: Source path does not exist or is not a directory.")
        return
    if not os.path.exists(destination_path) or not os.path.isdir(destination_path):
        print("Error: Destination path does not exist or is not a directory.")
        return

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Insert the new configuration into the configuration table
    try:
        c.execute("INSERT INTO configuration (section, path, filter, destination_path, destination_subdirectory) VALUES (?, ?, ?, ?, ?)",
                  (section, path, filter_val, destination_path, destination_subdirectory))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Section name must be unique.")
        conn.rollback()
        conn.close()
        return

    # Create directories for the new source and destination
    source_directory = os.path.abspath(path)
    destination_directory = os.path.abspath(os.path.join(destination_path, destination_subdirectory))

    try:
        os.makedirs(source_directory, exist_ok=True)
        os.makedirs(destination_directory, exist_ok=True)
    except OSError as e:
        print(f"Error creating directories: {e}")
        conn.close()
        return

    print("New source and destination directories created.")

    # Fetch the details of the newly added source and destination from the database
    c.execute("SELECT * FROM configuration WHERE section = ?", (section,))
    new_config = c.fetchone()

    conn.close()
    if new_config:
        print("New source and destination configuration added successfully:")
        print(f"Section: {new_config[1]}")
        print(f"Source Path: {new_config[2]}")
        print(f"Filter: {new_config[3]}")
        print(f"Destination Path: {new_config[4]}")
        print(f"Destination Subdirectory: {new_config[5]}")
    else:
        print("Failed to fetch the details of the newly added source and destination.")

if __name__ == '__main__':
    db_file = 'config.db'

    # Create the database if it doesn't exist
    create_database(db_file)

    # Prompt user for new configuration details and insert into the database
    insert_new_configuration(db_file)

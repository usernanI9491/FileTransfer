import configparser
import sqlite3

def create_database(db_file):
    """
    Create the SQLite database and table to store the configuration.
    """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS configuration
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  section TEXT,
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

def read_config(config_file, db_file):
    """
    Read the configuration from the config.ini file and store it in the SQLite database.
    """
    create_database(db_file)

    config = configparser.ConfigParser()
    config.read(config_file)

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    for section in config.sections():
        if section.startswith('Source'):
            path = config.get(section, 'Path')
            filter_val = config.get(section, 'Filter')
            enable = config.getboolean(section, 'Enable', fallback=True)  # Use getboolean to parse boolean values
            destination_section = section.replace('Source', 'Destination')
            destination_path = config.get(destination_section, 'Path')
            destination_subdirectory = config.get(destination_section, 'Subdirectory')

            c.execute("INSERT INTO configuration (section, path, filter, destination_path, destination_subdirectory, enabled) VALUES (?, ?, ?, ?, ?, ?)",
                     (section, path, filter_val, destination_path, destination_subdirectory, int(enable)))  # Cast enable to int

    conn.commit()
    conn.close()

    print("Configuration stored in the database.")

if __name__ == '__main__':
    read_config('config.ini', 'config.db')

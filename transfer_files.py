import os
import shutil
import sqlite3

def toggle_source_status(db_file):
    """
    Toggle the enable/disable status of sources based on user input.
    """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Fetch all sources from the database
    c.execute("SELECT section, enabled FROM configuration")
    sources = c.fetchall()

    conn.close()

    # Prompt user to enable or disable each source
    for source, enabled in sources:
        user_input = input(f"Enable source '{source}'? (y/n): ")
        enable_source = 1 if user_input.lower() == 'y' else 0
        if enable_source != enabled:
            update_source_status(db_file, source, enable_source)

def update_source_status(db_file, source_name, new_status):
    """
    Update the enable/disable status of a source in the database.
    """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Update the 'enabled' column for the specified source
    c.execute("UPDATE configuration SET enabled = ? WHERE section = ?", (new_status, source_name))
    conn.commit()

    conn.close()

def transfer_files(db_file):
    """
    Transfer files based on the configuration stored in the SQLite database.
    """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute("SELECT section, path, filter, destination_path, destination_subdirectory, enabled FROM configuration")  # Select all sources
    all_sources = c.fetchall()

    for source in all_sources:
        section, path, filter_val, destination_path, destination_subdirectory, enabled = source

        # Check if both destination_path and destination_subdirectory are not None
        if destination_path is not None and destination_subdirectory is not None:
            destination_full_path = os.path.join(destination_path, destination_subdirectory)

            os.makedirs(destination_full_path, exist_ok=True)

            for file in os.listdir(path):
                if file.endswith(f".{filter_val}") and enabled:
                    src_file = os.path.join(path, file)
                    dst_file = os.path.join(destination_full_path, file)

                    if os.path.exists(dst_file):
                        print(f"File '{file}' already exists in '{destination_full_path}'. Skipping...")
                    else:
                        print(f"Transferring '{file}' from '{path}' to '{destination_full_path}'")
                        shutil.copy(src_file, dst_file)
                else:
                    print(f"File '{file}' of source '{section}' doesn't match the filter or is disabled. Skipping...")

        else:
            print("Warning: Missing destination path or subdirectory for a source.")

    conn.close()

if __name__ == '__main__':
    db_file = 'config.db'

    # Toggle the enable/disable status of sources based on user input
    toggle_source_status(db_file)

    # Transfer files based on the configuration
    transfer_files(db_file)

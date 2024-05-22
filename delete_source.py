
import sqlite3
import os
import shutil
# Connect to the SQLite3 database
conn = sqlite3.connect('config.db')
cursor = conn.cursor()

def delete_source_from_db(source_name):
    try:
        # SQL command to delete the source based on its name
        delete_query = f'DELETE FROM configuration WHERE section = ?'
        cursor.execute(delete_query, (source_name,))
        conn.commit()
        print(f'{source_name} source deleted from database successfully!')
    except sqlite3.Error as e:
        print(f'Error deleting source from database: {e}')


def delete_source_from_local(source_path):
    try:
        # Check if the source directory exists
        if os.path.exists(source_path):
            # Delete the source directory and its contents
            shutil.rmtree(source_path)
            print(f'{source_path} directory deleted from local machine successfully!')
        else:
            print(f'{source_path} directory does not exist.')
    except OSError as e:
        print(f'Error deleting source from local machine: {e}')
# Function to prompt user for deletion confirmation
def prompt_delete(source_name, source_path):
    while True:
        confirmation = input(f'Do you want to delete {source_name} source? (y/n): ').lower()
        if confirmation == 'y':
            delete_source_from_db(source_name)
            delete_source_from_local(source_path)
            break
        elif confirmation == 'n':
            break
        else:
            print('Invalid input. Please enter "y" for yes or "n" for no.')

# Fetch all sources from the database
cursor.execute("SELECT section, path FROM configuration WHERE section LIKE 'Source%'")
sources = cursor.fetchall()

# Iterate over each source and prompt for deletion
for source in sources:
    source_name, source_path = source[0], source[1]
    prompt_delete(source_name, source_path)

# Close the database connection
conn.close()

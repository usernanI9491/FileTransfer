import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('config.db')

# Create a cursor object
c = conn.cursor()

# Execute query to fetch table names
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()

# Print table names
print("Tables in the database:")
for table in tables:
    print(table[0])

# Function to fetch and display content of a table
def display_table_content(table_name):
    c.execute(f"SELECT * FROM {table_name};")
    table_content = c.fetchall()
    print(f"\nContent of table '{table_name}':")
    for row in table_content:
        print(row)

# Display content of each table
for table in tables:
    display_table_content(table[0])

# Close cursor and connection
c.close()
conn.close()

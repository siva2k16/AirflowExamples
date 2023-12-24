import sqlite3

# Create a new SQLite database for the source
source_conn = sqlite3.connect('/mnt/data/source.db')
source_cursor = source_conn.cursor()

source_cursor.execute("""
CREATE TABLE IF NOT EXISTS source_table (
    id INTEGER PRIMARY KEY,
    data TEXT
)
""")

# Insert example data into source_table
source_cursor.execute("INSERT INTO source_table (data) VALUES ('First entry')")
source_cursor.execute("INSERT INTO source_table (data) VALUES ('Second entry')")

source_conn.commit()
source_conn.close()

# Create a new SQLite database for the destination
destination_conn = sqlite3.connect('/mnt/data/destination.db')
destination_cursor = destination_conn.cursor()

destination_cursor.execute("""
CREATE TABLE IF NOT EXISTS destination_table (
    id INTEGER PRIMARY KEY,
    data TEXT
)
""")

destination_conn.commit()
destination_conn.close()

def full_pull():
    # Connect to the source database
    source_conn = sqlite3.connect('/mnt/data/source.db')
    source_cursor = source_conn.cursor()

    # Fetch data from the source
    source_cursor.execute("SELECT * FROM source_table")
    data = source_cursor.fetchall()
    source_conn.close()

    # Connect to the target database and remove existing data
    destination_conn = sqlite3.connect('/mnt/data/destination.db')
    destination_cursor = destination_conn.cursor()
    destination_cursor.execute("DELETE FROM destination_table")

    # Insert data into the destination database
    destination_cursor.executemany("INSERT INTO destination_table (id, data) VALUES (?, ?)", data)
    destination_conn.commit()
    destination_conn.close()

# Execute the function to perform full data pull
full_pull()

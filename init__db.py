# init_db.py
import sqlite3

# Connect to the database file (it will be created if it doesn't exist)
connection = sqlite3.connect('database.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# To ensure a fresh start, we drop the old table if it exists
cursor.execute('DROP TABLE IF EXISTS certificates')

# Create the certificates table with student_id as the primary key
cursor.execute('''
CREATE TABLE certificates (
    student_id TEXT PRIMARY KEY,
    student_name TEXT NOT NULL,
    course_name TEXT NOT NULL,
    issue_date TEXT NOT NULL
);
''')

# --- Add Your Sample Certificate Data Here ---
print("Adding a certificate to the database...")

# New certificate data
cert_data = (
    'CA/MY3/1931',
    'Satyabrata Behera',
    'Machine Learning',
    '13th August 2025'
)

try:
    cursor.execute("""
        INSERT INTO certificates (student_id, student_name, course_name, issue_date)
        VALUES (?, ?, ?, ?)
    """, cert_data)
    print("Certificate added successfully.")
except sqlite3.IntegrityError:
    print(f"Error: A certificate with the Student ID '{cert_data[0]}' already exists.")


# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database script finished and connection closed.")

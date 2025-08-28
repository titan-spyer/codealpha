from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
import os

app = Flask(__name__)
# A secret key is required for flashing messages
# It's better to load this from an environment variable for security
app.secret_key = os.environ.get('SECRET_KEY', 'a-default-secret-key-for-dev')

DATABASE_FILE = 'database.db'

def get_db_connection():
    """
    Establishes a new connection to the database if one doesn't exist
    for the current application context.
    """
    # The 'g' object is unique for each request.
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_FILE)
        # This makes the cursor return rows that can be accessed by column name
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db_connection(exception=None):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_certificate_by_student_id(student_id):
    """Fetches a single certificate's data from the database by student ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # The '?' is the placeholder for parameters in SQLite
    query = "SELECT student_id, student_name, course_name, issue_date FROM certificates WHERE student_id = ?"
    cursor.execute(query, (student_id,))
    certificate = cursor.fetchone()
    # The connection is now closed automatically by the teardown_appcontext function
    return certificate

@app.route('/')
def index():
    """Renders the certificate verification page."""
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    """Handles verification and redirects to the certificate page on success."""
    student_id = request.form.get('student_id', '').strip()
    
    if not student_id:
        flash("Please enter a Student ID.", "error")
        return redirect(url_for('index'))
    
    # We can simplify this by redirecting directly. The show_certificate route will handle non-existent IDs.
    return redirect(url_for('show_certificate', student_id=student_id))

@app.route('/certificate/<path:student_id>')
def show_certificate(student_id):
    """Displays the details of a verified certificate on its own page."""
    certificate = get_certificate_by_student_id(student_id)
    if certificate:
        return render_template('certificate.html', certificate=certificate)
    else:
        # Flash a message and redirect for a better user experience
        flash(f"Student ID '{student_id}' not found. Please check the ID and try again.", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

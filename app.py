from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from functools import lru_cache

app = Flask(__name__)
# A secret key is required for flashing messages
# It's better to load this from an environment variable for security
app.secret_key = os.environ.get('SECRET_KEY', 'a-super-secret-key-for-dev')

# --- Data Loading Setup ---
# On a serverless platform like Vercel, we can't use a local SQLite file
# because the filesystem is read-only and ephemeral.
# Instead, we load the data from a JSON file that is part of the deployment.
CERTIFICATES_FILE = 'certificates.json'

@lru_cache() # Cache the result so we don't read the file on every request
def load_certificates_data():
    """
    Loads certificate data from the JSON file.
    The lru_cache decorator ensures this file is only read from disk once
    per serverless function instance, which is very efficient.
    """
    try:
        with open(CERTIFICATES_FILE, 'r', encoding='utf-8') as f:
            # Create a dictionary for fast lookups by student_id
            data = json.load(f)
            return {item['student_id']: item for item in data}
    except (FileNotFoundError, json.JSONDecodeError):
        # In case the file is missing or corrupt, return an empty dict
        return {}

def get_certificate_by_student_id(student_id):
    """Fetches a single certificate's data from the database by student ID."""
    all_certificates = load_certificates_data()
    return all_certificates.get(student_id)

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

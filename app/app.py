from flask import Flask, g
import sqlite3
import os
from datetime import datetime
import logging

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), '../data/requests.db')

# Set up logging
log_dir = os.path.join(os.path.dirname(__file__), '../logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename=os.path.join(log_dir, 'app.log'), level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Function to initialize the database
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL
            )
        ''')
        db.commit()
        logging.info('Database initialized')

# Function to query the database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Route for the root URL
@app.route('/')
def hello_world():
    db = get_db()
    cursor = db.cursor()

    # Get the current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert the current request time into the database
    cursor.execute('INSERT INTO requests (timestamp) VALUES (?)', (current_time,))
    db.commit()

    # Get the previous request time and the total number of requests
    cursor.execute('SELECT timestamp FROM requests ORDER BY id DESC LIMIT 2')
    rows = cursor.fetchall()
    previous_time = rows[1][0] if len(rows) > 1 else 'No previous requests'
    total_requests = query_db('SELECT COUNT(*) FROM requests', one=True)[0]

    # Log the request details
    logging.info(f'Current time: {current_time}, Previous request time: {previous_time}, Total requests: {total_requests}')

    # Close the database connection
    cursor.close()

    # Return the response
    return f'Hello, World! Current time: {current_time}, Previous request time: {previous_time}, Total requests: {total_requests}'

# Initialize the database before the first request
@app.before_request
def before_request():
    if not hasattr(g, 'db_initialized'):
        init_db()
        g.db_initialized = True

# Close the database connection when the application context ends
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')


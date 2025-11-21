def emit_poll_update():
    # Emits a Socket.IO event to all clients to refresh the poll chart
    socketio.emit('poll_update')
from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit

import matplotlib.pyplot as plt
import io
import os
import sqlite3

app = Flask(__name__, static_url_path='/static', static_folder='static')
socketio = SocketIO(app)

# Path to poll_stats.db inside GrimMonitor directory
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'poll_stats.db'))

@app.route('/')
def index():
    # Check if poll_stats.db exists and has data
    has_data = False
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM poll_stats')
            count = c.fetchone()[0]
            if count > 0:
                has_data = True
            conn.close()
        except Exception:
            has_data = False
    return render_template('index.html', has_data=has_data)

@app.route('/poll_chart.png')
def poll_chart():
    # Load poll stats from SQLite database
    poll_log = []
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT timestamp, total_votes FROM poll_stats ORDER BY timestamp ASC')
            poll_log = c.fetchall()
            conn.close()
        except Exception:
            poll_log = []
    # poll_log is a list of (timestamp, total_votes)
    if poll_log:
        timestamps, votes = zip(*poll_log)
        plt.style.use('dark_background')
        plt.figure(figsize=(8, 4))
        plt.plot(timestamps, votes, marker='o', color='#00bcd4')
        plt.title('Poll Votes Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Total Votes')
        plt.tight_layout()
    else:
        plt.style.use('dark_background')
        plt.figure(figsize=(8, 4))
        plt.text(0.5, 0.5, 'No poll data available', ha='center', va='center', fontsize=18, color='#888')
        plt.axis('off')
        plt.tight_layout()
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)

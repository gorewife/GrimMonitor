from flask import Flask, render_template, send_file
import matplotlib.pyplot as plt
import io
import os
import json

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Example: path to your poll log (adjust as needed)
POLL_LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../poll_log.json'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/poll_chart.png')
def poll_chart():
    # Load poll log data
    if os.path.exists(POLL_LOG_PATH):
        with open(POLL_LOG_PATH, 'r') as f:
            poll_log = json.load(f)
    else:
        poll_log = []
    # poll_log is a list of [timestamp, total_votes]
    if poll_log:
        timestamps, votes = zip(*poll_log)
    else:
        timestamps, votes = [], []
    # Plot
    plt.figure(figsize=(8, 4))
    plt.plot(timestamps, votes, marker='o')
    plt.title('Poll Votes Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Total Votes')
    plt.tight_layout()
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

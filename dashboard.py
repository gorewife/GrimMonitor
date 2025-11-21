from flask import Flask, send_file, render_template_string
import os
import json
from visualization_utils import plot_player_activity, plot_poll_usage

app = Flask(__name__)

# Paths to your stats files (update as needed)
PLAYER_ACTIVITY_FILE = 'player_activity_log.json'  # list of [timestamp, player_count]
POLL_LOG_FILE = 'poll_log.json'  # list of [timestamp, votes_count]

@app.route('/')
def index():
    return render_template_string('''
        <h1>Discord Bot Stats Dashboard</h1>
        <ul>
            <li><a href="/player-activity">Player Activity Over Time</a></li>
            <li><a href="/poll-usage">Poll Usage</a></li>
        </ul>
    ''')

@app.route('/player-activity')
def player_activity():
    if not os.path.exists(PLAYER_ACTIVITY_FILE):
        return 'No player activity data.'
    with open(PLAYER_ACTIVITY_FILE) as f:
        data = json.load(f)
    buf = plot_player_activity(data)
    if not buf:
        return 'No data to plot.'
    return send_file(buf, mimetype='image/png')

@app.route('/poll-usage')
def poll_usage():
    if not os.path.exists(POLL_LOG_FILE):
        return 'No poll usage data.'
    with open(POLL_LOG_FILE) as f:
        data = json.load(f)
    buf = plot_poll_usage(data)
    if not buf:
        return 'No data to plot.'
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

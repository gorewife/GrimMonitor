import matplotlib.pyplot as plt
import io
import datetime
from collections import Counter

def plot_player_activity(player_activity_log):
    """
    player_activity_log: list of (timestamp, player_count)
    """
    if not player_activity_log:
        return None
    # Sort by timestamp
    player_activity_log.sort()
    times = [datetime.datetime.fromtimestamp(ts) for ts, _ in player_activity_log]
    counts = [count for _, count in player_activity_log]
    plt.figure(figsize=(8,4))
    plt.plot(times, counts, marker='o', color='blue')
    plt.title('Player Activity Over Time')
    plt.xlabel('Time')
    plt.ylabel('Active Players')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def plot_poll_usage(poll_log):
    """
    poll_log: list of (timestamp, votes_count)
    """
    if not poll_log:
        return None
    # Aggregate by day
    day_counts = Counter(datetime.datetime.fromtimestamp(ts).date() for ts, _ in poll_log)
    days = sorted(day_counts)
    counts = [day_counts[day] for day in days]
    plt.figure(figsize=(8,4))
    plt.bar(days, counts, color='green')
    plt.title('Polls Created Per Day')
    plt.xlabel('Date')
    plt.ylabel('Polls Created')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

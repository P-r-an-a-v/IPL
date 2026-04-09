from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import random
import os

app = Flask(__name__)
# CORS allows your frontend to request data from this backend
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory('assets', path)

# Global mock state for live fluctuations
runs = 160
wickets = 4
overs = 17.2

@app.route('/api/live-score')
def get_live_score():
    global runs, wickets, overs
    
    # Simulate a ball being bowled
    runs += random.randint(0, 6)
    if random.random() < 0.05: # 5% chance of wicket
        wickets = min(10, wickets + 1)
        
    # Increment over properly
    overs_str = str(overs).split('.')
    balls = int(overs_str[1]) if len(overs_str) > 1 else 0
    if balls == 5:
        overs = int(overs_str[0]) + 1.0
    else:
        overs = round(overs + 0.1, 1)
        
    current_run_rate = round(runs / (int(str(overs).split('.')[0]) + (balls/6) + 0.1), 2)
    projected_score = int(current_run_rate * 20)
    
    recent_balls = ["1", "4", "0", "W", "2", "6"]
    random.shuffle(recent_balls)
    
    # Generate mock run accumulation for the chart (runs per over history)
    # The sum of this array should ideally match the total runs, but we'll mock a smooth curve
    runs_per_over = [
        8, 12, 5, 20, 4, 9, 7, 14, 6, 8, 10, 3, 11, 7, 15, 9, 13
    ]
    # Append the running over history for frontend to draw a chart
    
    response_data = {
        "match": {
            "title": "CSK vs MI",
            "venue": "M. A. Chidambaram Stadium, Chennai",
            "status": "In Progress - Innings 1"
        },
        "scoreSummary": {
            "battingTeam": "CSK",
            "bowlingTeam": "MI",
            "runs": runs,
            "wickets": wickets,
            "overs": overs,
            "currentRunRate": current_run_rate,
            "requiredRunRate": None,
            "projectedScore": projected_score
        },
        "chartData": {
            "labels": [f"Ov {i+1}" for i in range(len(runs_per_over))],
            "runsPerOver": runs_per_over
        },
        "activeBatsmen": [
            {
                "name": "M. S. Dhoni",
                "runs": random.randint(45, 60),
                "balls": random.randint(20, 25),
                "isStriker": True
            },
            {
                "name": "R. Jadeja",
                "runs": random.randint(15, 25),
                "balls": random.randint(8, 12),
                "isStriker": False
            }
        ],
        "activeBowler": {
            "name": "J. Bumrah",
            "overs": 3.2,
            "maidens": 0,
            "runsConceded": random.randint(18, 28),
            "wickets": random.randint(1, 3)
        },
        "recentDeliveries": recent_balls[:6]
    }
    
    return jsonify(response_data)

@app.route('/api/standings')
def get_standings():
    # Mock data for points table
    teams = [
        {"team": "RR", "played": 14, "won": 10, "lost": 4, "pts": 20, "nrr": "+0.563"},
        {"team": "CSK", "played": 14, "won": 9, "lost": 5, "pts": 18, "nrr": "+0.320"},
        {"team": "MI", "played": 14, "won": 8, "lost": 6, "pts": 16, "nrr": "+0.114"},
        {"team": "RCB", "played": 14, "won": 7, "lost": 7, "pts": 14, "nrr": "+0.045"},
        {"team": "SRH", "played": 14, "won": 7, "lost": 7, "pts": 14, "nrr": "-0.081"},
        {"team": "LSG", "played": 14, "won": 6, "lost": 8, "pts": 12, "nrr": "-0.240"},
        {"team": "DC", "played": 14, "won": 5, "lost": 9, "pts": 10, "nrr": "-0.321"},
        {"team": "PBKS", "played": 14, "won": 4, "lost": 10, "pts": 8, "nrr": "-0.540"},
    ]
    return jsonify(teams)

@app.route('/api/players')
def get_players():
    # Mock infographics data
    players = [
        {
            "name": "Virat Kohli",
            "team": "RCB",
            "role": "Batsman",
            "matches": 240,
            "runs": 7443,
            "strikeRate": 130.5,
            "highScore": 113,
            "hundreds": 7
        },
        {
            "name": "M. S. Dhoni",
            "team": "CSK",
            "role": "Wicketkeeper Batter",
            "matches": 255,
            "runs": 5120,
            "strikeRate": 136.2,
            "highScore": 84,
            "hundreds": 0
        },
        {
            "name": "J. Bumrah",
            "team": "MI",
            "role": "Bowler",
            "matches": 125,
            "runs": 65, # Doesn't bat much
            "strikeRate": 80.0,
            "wickets": 150,
            "economy": 7.39
        }
    ]
    return jsonify(players)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

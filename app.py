
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load dataset for dropdowns
df = pd.read_csv("matches.csv")

# Extract unique values
team_names = sorted(df['team1'].dropna().unique().tolist())
city_names = sorted(df['city'].dropna().unique().tolist())
venue_names = sorted(df['venue'].dropna().unique().tolist())

# Create mappings (label encoders used during training)
team_mapping = {team: idx for idx, team in enumerate(team_names)}
city_mapping = {city: idx for idx, city in enumerate(city_names)}
venue_mapping = {venue: idx for idx, venue in enumerate(venue_names)}

@app.route('/')
def index():
    return render_template("index4.html",
                           teams=team_mapping,
                           cities=city_mapping,
                           venues=venue_mapping)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    input_data = np.array([[ 
        int(data['city']),
        int(data['venue']),
        int(data['team1']),
        int(data['team2']),
        int(data['toss_winner']),
        int(data['toss_decision']),
        float(data['target_runs']),
        float(data['target_overs']),
        int(data['home_advantage_team1']),
        int(data['home_advantage_team2'])
    ]])

    prediction = model.predict(input_data)[0]

    # You can map the prediction back to team name if needed
    predicted_team = list(team_mapping.keys())[list(team_mapping.values()).index(prediction)]

    return jsonify({
        "predicted_winner_encoded": int(prediction),
        "predicted_team": predicted_team
    })

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
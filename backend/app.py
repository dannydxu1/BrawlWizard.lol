from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
load_dotenv()

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

@app.route('/api/brawler_data', methods=['GET'])
def get_brawler_data():
    try:
        # Read the CSV file
        df = pd.read_csv('brawler_data.csv')
        # Extract the desired columns
        result = df[['brawler_id', 'win_rate', 'usage_rate', 'rank']].to_dict(orient='records')
        return jsonify(result), 200
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route('/api/player/<player_tag>', methods=['GET'])
def get_player_data(player_tag):
    try:
        api_key = os.getenv('BRAWL_STARS_API_KEY')
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        url = f'https://api.brawlstars.com/v1/players/%23{player_tag}'
        print("Request received", url)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return jsonify(error='Failed to retrieve player data'), response.status_code

        player_data = response.json()

        # Extract the required fields
        filtered_data = {
            "tag": player_data.get("tag"),
            "name": player_data.get("name"),
            "trophies": player_data.get("trophies"),
            "highestTrophies": player_data.get("highestTrophies"),
            "3vs3Victories": player_data.get("3vs3Victories"),
            "soloVictories": player_data.get("soloVictories"),
            "duoVictories": player_data.get("duoVictories"),
            "club": player_data.get("club")
        }

        # Get the top 5 brawlers by trophies
        brawlers = player_data.get("brawlers", [])
        top_brawlers = sorted(brawlers, key=lambda x: x.get("trophies", 0), reverse=True)[:5]
        filtered_data["topBrawlers"] = top_brawlers

        return jsonify(filtered_data), 200
    except Exception as e:
        return jsonify(error=str(e)), 500



if __name__ == '__main__':
    app.run(debug=True)

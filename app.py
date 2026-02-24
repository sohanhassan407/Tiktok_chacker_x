from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import re

app = Flask(__name__)
CORS(app)

def format_number(num_str):
    """Converts TikTok's K, M, B strings to integers."""
    if not num_str: return 0
    num_str = num_str.upper()
    multiplier = 1
    if 'K' in num_str: multiplier = 1000
    elif 'M' in num_str: multiplier = 1000000
    elif 'B' in num_str: multiplier = 1000000000
    
    clean_num = re.sub(r'[^\d.]', '', num_str)
    return int(float(clean_num) * multiplier) if clean_num else 0

@app.route('/api/stats', methods=['GET'])
def get_tiktok_stats():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    url = f"https://www.tiktok.com/@{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_status != 200:
            return jsonify({"error": "User not found"}), 404

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Finding the JSON data inside the script tag
        script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__')
        if not script_tag:
            return jsonify({"error": "Data unavailable"}), 404
            
        data = json.loads(script_tag.string)
        user_info = data['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']['stats']

        followers = user_info.get('followerCount', 0)
        likes = user_info.get('heartCount', 0)
        videos = user_info.get('videoCount', 0)
        
        # Simulated logic for Avg Views based on recent engagement
        # (Real view counts require iterating through the video list)
        avg_views = int((likes * 1.5) / (videos if videos > 0 else 1))

        return jsonify({
            "followers": followers,
            "likes": likes,
            "video_count": videos,
            "avg_views": avg_views
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

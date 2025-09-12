from flask import Flask, request, jsonify
import argparse
from flask_cors import CORS
import threading
import traceback
from routes.twitter import postInitiateTwitterScrap
from routes.youtube import youtubeScrapper
from routes.facebook import facebookScraper
from config.db_model import twitterTokens
from routes.threads import threadScraper
from routes.reddit import redditScrapper

app = Flask(__name__)
CORS(app)

app.register_blueprint(youtubeScrapper)
app.register_blueprint(threadScraper)
# app.register_blueprint(getScrapSessionData)
app.register_blueprint(facebookScraper)
app.register_blueprint(redditScrapper)
app.register_blueprint(postInitiateTwitterScrap)

is_server_busy = False

crawling_routes = {
    'youtubeScrapper.youtubeScrapperFunc',
    'postInitiateTwitterScrap.InitiateTwitterScrap',
    'facebookScraper.facebookScrapFunc',
    'dailyMotionScraper',
    'instaScrapper',
    'telegramScraper'
}

@app.before_request
def before_request():
    print(f"Request Received : {request.endpoint}")
    global is_server_busy
    if request.endpoint in crawling_routes:
        is_server_busy = True  

@app.after_request
def after_request(response):
    global is_server_busy
    print(f"Request Termination : {request.endpoint}")
    if request.endpoint in crawling_routes:
        is_server_busy = False
    return response

@app.route('/status')
def status():
    return jsonify({'busy': is_server_busy})

@app.route('/uploadTokens', methods=['POST'])
def submit_data():
    accepted_platforms = ["twitter","facebook","threads"]
    try:
        data = request.json
        platform = data.get('platform')
        if platform is None or platform=="" or platform not in accepted_platforms:
            return "Invalid/missing platform",400
        if platform=='twitter':
            required_fields = ['token', 'user_agent', 'username']

            for field in required_fields:
                if not data.get(field):
                    return jsonify({"message": f"Missing required field: {field}"}), 400
            token = data.get('token')
            user_agent = data.get('user_agent')
            username = data.get('username')
            twitterTokens.insert_one({
                "token":token,
                "user_agent":user_agent,
                "username":username
            })
            return jsonify({"message":"Token Uploaded Successfully"}),200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message":f"Failed to Upload Token {e} "}),500
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Flask app with custom port')
    parser.add_argument('--port', type=int, default=5001, help='Port number (default: 5000)')
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=9090, debug=True)
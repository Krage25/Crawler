from flask import Blueprint, jsonify,request
import random
from platforms.youtube.youyubeAPI import youtube_search_with_comments 
import threading
from datetime import datetime
from utilities.authenticate import authenticate_token
from utilities.logger import Logger
import traceback


youtubeScrapper = Blueprint('youtubeScrapper', __name__)
log=Logger()

@youtubeScrapper.route('/youtubeScrapper', methods=['POST'])
def youtubeScrapperFunc():
    log.warning("Youtube Crawling Started")
    try:
        data = request.json
        auth_header = request.headers.get("Authorization")
        token = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            return jsonify({"error": "Authorization token missing or malformed"}), 401

        # Validate the token
        try:
            payload = authenticate_token(token)
            username = payload['username']
        except Exception as auth_error:
            return jsonify({"error": str(auth_error)}), 401
        
        keywords = data.get('keywords')
        dataCount = data.get('postCount')
        sessionId = data.get('sessionId')
        required_params = ['keywords', 'postCount', 'sessionId']
        missing_params = [param for param in required_params if not data.get(param)]

        if missing_params:
            return jsonify({
                "error": "Missing required parameters",
                "missing": missing_params
            }), 400
        # cleaned_keyword =[remove_hashtags(keyword) for keyword in keywords]
        # username = "damru"
        results = []
        if keywords:
            for keyword in keywords:
                results.extend(youtube_search_with_comments(keyword, sessionId, dataCount,username))
        else:
            raise ValueError("Keywords are missing") 
        # filtered_results = [res for res in results if res]

        if not results:
            return '', 204

        return jsonify(results), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({f"message": "Server error :{e} "}), 500  


 
    
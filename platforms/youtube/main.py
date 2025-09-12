from flask import Blueprint, jsonify,request
from Exceptions.authorization import InvalidTokenError, NotAuthorizedError
import random
from Youtube_Scrapper.youtube_selenium_module import youtube_selenium_module
import threading
from utility_functions.removeHashtags import remove_hashtags
from datetime import datetime
from InfoAPI.createSessionData import createSessionData
from InfoAPI.updateSessionData import updateSessionData
from AuthenticationAPI.helper_functions.authorization import validate_token
from utility_functions.chromeKiller import cleanup_chrome_processes
from Twitter_Scrapper import global_data
# from Twitter_Scrapper import 
from utility_functions.ExecuteBeforeTimeout import handle_timeout
from authenticate import authenticate_token
from Twitter_Scrapper.logger import Logger
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
                results.extend(youtube_selenium_module(keyword, sessionId, dataCount,username))
        else:
            raise ValueError("Keywords are missing") 
        # filtered_results = [res for res in results if res]

        if not results:
            return '', 204

        return jsonify(results), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({f"message": "Server error :{e} "}), 500  


 
    
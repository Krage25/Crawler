from flask import Blueprint, jsonify,request
import random
import threading
from datetime import datetime
from platforms.facebook.selenium_module import facebook_selenium_module
import threading
from utilities.googleSerachAPI import webSearch
import traceback
from utilities.authenticate import authenticate_token

facebookScraper = Blueprint('facebookScraper', __name__)
# logger = configure_logger("login_logger",'logs/login.log', logging.INFO)

@facebookScraper.route('/facebookScraper', methods=['POST'])
def FacebookScraper():
    try:
        data = request.json
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization token missing or malformed"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = authenticate_token(token)
            username = payload['username']
        except Exception as auth_error:
            return jsonify({"error": str(auth_error)}), 401
        
        required_params = ['keywords', 'postCount', 'sessionId']
        missing_params = [param for param in required_params if not data.get(param)]
        if missing_params:
            return jsonify({
                "error": "Missing required parameters",
                "missing": missing_params
            }), 400

        keywords = data.get('keywords')
        dataCount = data.get('postCount')
        sessionId = data.get('sessionId')

        results = []
        for keyword in keywords:
                Links = webSearch(f"site:facebook.com {keyword}",dataCount)
                filtered_links = []
                for l in Links :
                    link = l['link']
                    if link:
                        filtered_links.append(link)
                result = facebook_selenium_module(filtered_links, keyword, sessionId, dataCount, username)
                if result:
                    results.extend(result)

        print(f"Length Of Data Crawled : {len(results)}")
        if not results:
            return jsonify({"message":"No Data Found for The Given Keyword"}),200
        return jsonify(results), 200
    except Exception as e: 
        traceback.print_exc()
        return jsonify({"message": f"Server error: {str(e)}"}), 500  

    
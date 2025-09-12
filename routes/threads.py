from flask import Blueprint, jsonify,request
import random
import threading
from datetime import datetime
from platforms.threads.thread_selenium_module import threadScrapper
import threading
from utilities.authenticate import authenticate_token

threadScraper = Blueprint('threadScraper', __name__)
# logger = configure_logger("login_logger",'logs/login.log', logging.INFO)

@threadScraper.route('/threadScraper', methods=['POST'])
def redditScrapperFunc():
    try:
        data = request.json
        auth_header = request.headers.get("Authorization")
        token = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            return jsonify({"error": "Authorization token missing or malformed"}), 401
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
        results = []
        if keywords:
            threads = []
            for keyword in keywords:
                results.extend(threadScrapper(keyword, sessionId, dataCount,username))
        else:
            raise ValueError("Keywords are missing")
        return results,200
        
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except FileNotFoundError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Server error"}), 500  

    
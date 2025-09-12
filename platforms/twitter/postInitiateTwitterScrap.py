from flask import Blueprint, jsonify,request
from Exceptions.authorization import InvalidTokenError, NotAuthorizedError
import random
from Twitter_Scrapper.index import main
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
from Exceptions.customException import TwitterTokenExpiredException
import traceback
from createSession import createSessionData
from updateSession import updateSessionData
import time
import sys

postInitiateTwitterScrap = Blueprint('postInitiateTwitterScrap', __name__)
log=Logger()

@postInitiateTwitterScrap.route('/postInitiateTwitterScrap', methods=['POST'])
def InitiateTwitterScrap():
    log.warning("Twitter Crawling Started")
    # return jsonify({"message":"Crawling Failed"}),500
    
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
        dateCurrent = datetime.now()
        
        print("Stopped Before Creating Session")
        sys.exit()
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
        createSessionData(sessionId, dateCurrent, keywords,"twitter","sentiment")
        print(f"keywords:{keywords}")
        # cleaned_keywords = [remove_hashtags(keyword) for keyword in keywords]
        results = []
        for keyword in keywords:
            try:
                result = main(keyword, sessionId, dataCount, "username")
                if result:
                    results.extend(result)
            except TwitterTokenExpiredException:
                return jsonify({"error": "Twitter token expired"}), 401
            except Exception as scrape_error:
                log.error(f"Error scraping for keyword '{keyword}': {scrape_error}")
                continue  
        print(f"Length Of Data Crawled : {len(results)}")
        timeTaken = datetime.now()- dateCurrent
        updateSessionData("hgkjdschkdhvkhdvi",sessionId, keywords, "twitter", timeTaken)
        if not results:
            return jsonify({"message":"Crawling Failed"}),500
        return jsonify(results), 200
    except Exception as e: 
        traceback.print_exc()
        log.exception("Unhandled error in InitiateTwitterScrap")
        return jsonify({"message": f"Server error: {str(e)}"}), 500
    



 
    
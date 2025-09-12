from flask import Blueprint, jsonify,request
import random
from platforms.twitter.index import main
import threading
from utilities.removeHashtags import remove_hashtags
from datetime import datetime
from utilities.authenticate import authenticate_token
from utilities.logger import Logger
import traceback
import time
from createSession import createSessionData
from updateSession import updateSessionData

postInitiateTwitterScrap = Blueprint('postInitiateTwitterScrap', __name__)
log=Logger()

@postInitiateTwitterScrap.route('/postInitiateTwitterScrap', methods=['POST'])
def InitiateTwitterScrap():
    log.warning("Twitter Crawling Started")
    # return jsonify({"message":"Crawling Failed"}),500
    try:
        data = request.json
        
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
        dateCurrent = datetime.now()
        # createSessionData(sessionId, dateCurrent, keywords,"twitter","sentiment")
        # cleaned_keywords = [remove_hashtags(keyword) for keyword in keywords]
        results = []
        for keyword in keywords:
            try:
                result = main(keyword, sessionId, dataCount, "karan")
                if result:
                    results.extend(result)
            except Exception as e:
                return jsonify({"error": "Twitter token expired"}), 401
            except Exception as scrape_error:
                log.error(f"Error scraping for keyword '{keyword}': {scrape_error}")
                continue  
        print(f"Length Of Data Crawled : {len(results)}")
        # timeTaken = datetime.now()- dateCurrent
        # updateSessionData("hgkjdschkdhvkhdvi",sessionId, keywords, "twitter", timeTaken)
        if not results:
            return jsonify({"message":"Crawling Failed"}),500
        return jsonify(results), 200
    except Exception as e:
        traceback.print_exc()
        log.error(f"Unhandled error in InitiateTwitterScrap {e}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500
    



 
    
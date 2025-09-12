from flask import Blueprint, jsonify,request
from Exceptions.authorization import InvalidTokenError, NotAuthorizedError
import random
import threading
from datetime import datetime
from InfoAPI.createSessionData import createSessionData
from New_Reddit.selenium_module import reddit_main
import threading
from InfoAPI.updateSessionData import updateSessionData

redditScrapper = Blueprint('redditScrapper', __name__)
# logger = configure_logger("login_logger",'logs/login.log', logging.INFO)

@redditScrapper.route('/redditScrapper', methods=['POST'])
def redditScrapperFunc():
    timeStarted = datetime.now()
    try:
        data = request.json
        keywords = data.get('keywords')
        sessionId=''.join(str(random.randint(0, 9)) for _ in range(12))
        objectId = createSessionData(sessionId, timeStarted, keywords,"reddit")

        if keywords:
            threads = []
            for keyword in keywords:
                thread = threading.Thread(target=reddit_main, args=(keyword,sessionId))
                threads.append(thread)
                thread.start()  
            
            for thread in threads:
                thread.join()
            timeTaken = datetime.now()-timeStarted
            updateSessionData(objectId, sessionId, keywords,"twitter", timeTaken)
            
        else:
            raise ValueError("Keywords are missing")
        return "Successfull",200
        
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except FileNotFoundError as e:
        return jsonify({"message": str(e)}), 404
    except InvalidTokenError as e:
        return jsonify({"message": str(e)}), 403
    except Exception as e:
        # logger.warning("login ==> %s",str(e)) 
        print(f"Error: {str(e)}")
        return jsonify({"message": "Server error"}), 500  

    
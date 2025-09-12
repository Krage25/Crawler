from config.db_model import youtubePosts, twitterPosts, dailymotionPosts, instagramPosts, facebookPosts
from config.db_model import sessionDetails
def createSessionData(sessionId, dateCreated, keywords,platform,sentimentType):
    print("Creating Session")
    try:
        # platformSelected = None
        # counts = 0
        # keywordCount = {}
        # if platform=="twitter":
        #     counts = twitterPosts.count_documents({"sessionId":sessionId})
            
        #     for key in keywords:
        #         count = twitterPosts.count_documents({"keyword":key, "sessionId":sessionId})
        #         keywordCount[key] = count
        # elif platform=="youtube":
        #     counts= youtubePosts.count_documents({"sessionId":sessionId})
            
        #     for key in keywords:
        #         count = twitterPosts.count_documents({"keyword":key, "sessionId":sessionId})
        #         keywordCount[key] = count
        # elif platform=="dailymotion":
        #     counts= dailymotionPosts.count_documents({"sessionId":sessionId})
            
        #     for key in keywords:
        #         count = twitterPosts.count_documents({"keyword":key, "sessionId":sessionId})
        #         keywordCount[key] = count
        # elif platform=="instagram":
        #     counts= instagramPosts.count_documents({"sessionId":sessionId})
            
        #     for key in keywords:
        #         count = instagramPosts.count_documents({"keyword":key, "sessionId":sessionId})
        #         keywordCount[key] = count
        # elif platform=="facebook":
        #     counts= facebookPosts.count_documents({"sessionId":sessionId})
            
        #     for key in keywords:
        #         count = facebookPosts.count_documents({"keyword":key, "sessionId":sessionId})
        #         keywordCount[key] = count

        
        data = {
            "sessionId":sessionId,
            "dateCreated":dateCreated,
            # "postCount":counts,
            "keywords":keywords,
            # "timeTaken":str(timeTaken),
            "status":0,
            "platform":platform,
            "type":sentimentType
            # "keywordCount":keywordCount
        }
        objectId = sessionDetails.insert_one(data).inserted_id
        return objectId
        
    except Exception as e:
        # logger.warning("login ==> %s",str(e)) 
        print(f"Error: {str(e)}")
        return e

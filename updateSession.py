from config.db_model import youtubePosts, twitterPosts, dailymotionPosts, instagramPosts, facebookPosts,scrappedPosts,DigiNews
from config.db_model import sessionDetails, pinterestPosts
from bson import ObjectId
from config.db_model import newsSession


newsChannels = ["ABP News","Dainik Bhaskar","Deccan Chronicles","Indian Express",
                "Muslim Mirror","News Laundry","News Minute","The Hindu","The Wire","Scroll","Al Jazeera",
                "Dainik Bhashkar","Nava Bharat Times","Deccan Herald","Rising Kashmir","The Print",
                "The Guardian","India Today","Desh Abhimani","Punjab Kesari","Hindustan Times","Free Press Journal",
                "Times Of India","Outlook"
                ]

def performChecks(platform):
    scrappedPosts.update_many(
                {
                    'platform': platform,
                    'languages': { '$in': ['Lang Detect Fail', 'Nepali'] }
                },
                {
                    '$set': { 'languages': 'English' }
                }
                )

def updateSessionData(objectId,sessionId, keywords, platform, timeTaken):
    print("Updating Session")
    print(f"Time Taken : {timeTaken}")
    print(f"Keywords :{keywords}")
    print(keywords)
    try:
        platformSelected = None
        counts = 0
        keywordCount = {}
        newsChannelCount = {}
        if platform=="twitter":
            performChecks('twitter')
            counts = scrappedPosts.count_documents({"sessionId":sessionId})
            for key in keywords:
                count = scrappedPosts.count_documents({"keyword":key, "sessionId":sessionId})
                keywordCount[key] = count
        elif platform=="youtube":
            performChecks('youtube')
            # scrappedPosts.delete_many({
            #         "sessionId": sessionId,
            #         "$or": [
            #             {"translation": "none"},
            #             {"languages": "Lang Detect Fail"}
            #         ]
            #     })

            counts= scrappedPosts.count_documents({"sessionId":sessionId})
            
            for key in keywords:
                count = scrappedPosts.count_documents({"keyword":key, "sessionId":sessionId})
                keywordCount[key] = count
        elif platform=="dailymotion":
            performChecks('dailymotion')
            counts= scrappedPosts.count_documents({"sessionId":sessionId})
            
            for key in keywords:
                count = scrappedPosts.count_documents({"keyword":key, "sessionId":sessionId})
                keywordCount[key] = count
        elif platform=="instagram":
            performChecks('instagram')
            counts= scrappedPosts.count_documents({"sessionId":sessionId})
            
            for key in keywords:
                count = scrappedPosts.count_documents({"keyword":key, "sessionId":sessionId})

                keywordCount[key] = count
        elif platform=="facebook":
            performChecks('facebook')
            counts= scrappedPosts.count_documents({"sessionId":sessionId})
            
            for key in keywords:
                count = scrappedPosts.count_documents({"keyword":key, "sessionId":sessionId})
                keywordCount[key] = count
        
        elif platform=="threads":
            performChecks('threads')
            counts= scrappedPosts.count_documents({"sessionId":sessionId})
            
            for key in keywords:
                count = scrappedPosts.count_documents({"keyword":key, "sessionId":sessionId})
                keywordCount[key] = count
        elif platform=="pinterest":
            counts= pinterestPosts.count_documents({"sessionId":sessionId})
            for key in keywords:
                count = pinterestPosts.count_documents({"keyword":key, "sessionId":sessionId})
                keywordCount[key] = count
        elif platform=="telegram":
            counts= scrappedPosts.count_documents({"sessionId":sessionId})
            for key in keywords:
                count = scrappedPosts.count_documents({"keyword":key, "sessionId":sessionId})
                keywordCount[key] = count
        elif platform=="News":
            DigiNews.delete_many({"sessionId":sessionId, "content":"none"})
            counts= DigiNews.count_documents({"sessionId":sessionId})
            for channels in newsChannels:
                count = DigiNews.count_documents({"newsChannel":channels, "sessionId":sessionId})
                if(count==0):
                    continue
                newsChannelCount[channels] = count
        
        if counts==0:
            sessionDetails.delete_one({"sessionId":sessionId})
            return

        if platform!="News":
            sessionDetails.update_one(
                {"sessionId": sessionId },
                {
                    "$set": {
                        "keywordCount": keywordCount,
                        "postCount": counts,
                        "timeTaken":str(timeTaken),
                        "status":1
                    }
                }
            )
        else:
            newsSession.update_one(
                {"_id": ObjectId(objectId) },
                {
                    "$set": {
                        "newsChannelCount": newsChannelCount,
                        "articleCount": counts,
                        "timeTaken":str(timeTaken),
                        "status":1
                    }
                }
            )
        
    except Exception as e:
        # logger.warning("login ==> %s",str(e)) 
        print(f"Error: {str(e)}")
        return e
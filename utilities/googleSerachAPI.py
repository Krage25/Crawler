import traceback
import requests
# from db_model import FakeNewsTokens
from bson import ObjectId

# def getToken():
#     try:
#         return FakeNewsTokens.find_one({"hasCapacity": "true"})
#     except Exception:
#         traceback.print_exc()

# def updateExpiredTokens(token_id):
#     try:
#         FakeNewsTokens.update_one(
#             {"_id": ObjectId(token_id)},
#             {"$set": {"hasCapacity": "false"}}
#         )
#     except Exception:
#         traceback.print_exc()

def webSearch(query, total_results=30):
    api_key = "AIzaSyDLKUfMqtjqf0xsA4gdF0YTFtyfXtaVh7A"
    cse_id = "52a1a607959f44eff"
    
    try:
        # token = getToken()
        # if not token:
        #     raise Exception("No valid API token found.")

        # api_key = token['authKey']
        # cse_id = token['id']
        # token_id = str(token['_id'])

        url = "https://www.googleapis.com/customsearch/v1"
        output = []

        results_fetched = 0
        start_index = 1  # Google's pagination is 1-based

        while results_fetched < total_results:
            num = min(10, total_results - results_fetched)

            params = {
                "key": api_key,
                "cx": cse_id,
                "q": query,
                "sort": "date", 
                "num": num,
                "start": start_index,
                "location": "India",
            }

            response = requests.get(url, params=params)
            if response.status_code != 200:
                # updateExpiredTokens(token_id)
                # webSearch(query,30)
                raise Exception(f"API Error: {response.status_code} - {response.text}")

            data = response.json()
            items = data.get("items", [])

            if not items:
                break  # No more results to fetch

            for item in items:
                result_data = {
                    "title": item.get("title"),
                    "snippet": item.get("snippet"),
                    "link": item.get("link"),
                    "published_date": item.get("pagemap", {}).get("metatags", [{}])[0].get("article:published_time")
                }
                output.append(result_data)

            results_fetched += len(items)
            start_index += len(items)

           
            if len(items) < num:
                break

        return output[:total_results]

    except Exception:
        traceback.print_exc()
        return []

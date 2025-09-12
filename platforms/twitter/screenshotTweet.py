import os
# import pandas as pd
from requests_html import HTMLSession
from pyppeteer import launch
import asyncio
import time


screenshot_folder = r"static"

def screenshotTweet():
    print("Check")

    # Read CSV file
    # df = pd.read_csv('twitter_db.tweets.csv', encoding='latin1')

    # Initialize HTMLSession
    session = HTMLSession()

    # Launch browser with specified executable path
    browser = launch(executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe', args=['--ignore-certificate-errors'], headless=True)

    # images path
    
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)

    # Iterate
    # for link in links:
        url = "https://x.com/AmanTyagi167/status/1798282332224545178"
        # insertedId = link['id']
        page = browser.newPage()
        try:
            page.goto(url)

            # Wait for 5 seconds
            

            # Take screenshot
            screenshot_path = os.path.join('images', f'"Image".png')
            page.screenshot({'path': screenshot_path, 'fullPage': True})
            # print(f'Screenshot saved for URL at index {index}')
        except Exception as e:
            print(f"Error processing URL at index : {str(e)}")

    browser.close()
    session.close()

# asyncio.run(main())


# start = time.time()
# main()
# end = time.time()

# print(f"time taken: {round(end-start)} seconds")
screenshotTweet()
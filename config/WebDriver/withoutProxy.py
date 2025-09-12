import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from utilities.logger import Logger
from platforms.twitter.tweet import Tweet
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from bson import ObjectId
from selenium.common.exceptions import InvalidSessionIdException
from threading import Timer
from config.db_model import twitterTokens
import random
import traceback
from config.db_model import proxyIP, isProxy
import platform
import tempfile

log = Logger()

def open_driver_non_proxy(headless: bool, agent: str) -> uc.Chrome:
    try:
        system = platform.system()
        log.warning("Not Using Proxy IP")

        # Important: Don't mix Options from selenium.webdriver.chrome.options.Options
        # Instead, use uc.ChromeOptions
        options = uc.ChromeOptions()

        if system == "Windows":
            log.success("It's Windows. Nothing to worry, thanks to Bill Gates.")
        elif system == "Linux":
            print("Added Profile in Linux")
            user_data_dir = tempfile.mkdtemp(prefix="udc_profile_")
            options.add_argument(f"--user-data-dir={user_data_dir}")
        else:
            raise RuntimeError(f"Unsupported OS: {system}")

        options.add_argument('--log-level=3')
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--no-proxy-server')
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--disable-blink-features=AutomationControlled')  # further masks automation
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')

        if headless:
            options.add_argument('--headless=new')  

        options.add_argument(f"user-agent={agent}")

        # You can also add experimental preferences if needed
        # options.add_experimental_option("prefs", {...})

        driver = uc.Chrome(version_main=137,
            options=options,
            
            use_subprocess=True  
        )

        navigator_data = driver.execute_script("""
        let data = {};
        for (let prop in navigator) {
            try {
                let value = navigator[prop];
                if (typeof value !== 'object' && typeof value !== 'function') {
                    data[prop] = value;
                } else {
                    data[prop] = '[complex value skipped]';
                }
            } catch (e) {
                data[prop] = 'Error reading property';
            }
        }
        return data;
        """)

        import pprint
        pprint.pprint(navigator_data)

        plugins = driver.execute_script("return Array.from(navigator.plugins).map(p => p.name);")
        mimeTypes = driver.execute_script("return Array.from(navigator.mimeTypes).map(m => m.type);")

        print("Plugins:", plugins)
        print("MimeTypes:", mimeTypes)

        return driver

    except Exception:
        traceback.print_exc()
        raise

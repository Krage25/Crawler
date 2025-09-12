from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
import tempfile
import platform
import traceback
import time

def parse_proxy_url(proxy_url: str):
    """
    Parses a proxy string in the format:
    [http(s)://]username:password@host:port
    Returns: username, password, host, port
    """
    try:
        # Remove protocol if present
        if "://" in proxy_url:
            proxy_url = proxy_url.split("://", 1)[1]
        # Split at @
        auth_part, host_part = proxy_url.split("@", 1)
        # Split auth
        username, password = auth_part.split(":", 1)
        # Split host
        host, port = host_part.split(":", 1)
        return username, password, host, port
    except ValueError:
        raise ValueError(
            f"Invalid proxy format: '{proxy_url}'. Expected format is username:password@host:port"
        )

from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
import tempfile
import platform
import traceback
import time

def open_driver_with_proxy(headless: bool, agent: str, proxy_ip: str) -> Chrome:
    try:
        # Parse proxy components
        username, password, proxy_host, proxy_port = parse_proxy_url(proxy_ip)
        proxy_url = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
        print(f"Using Proxy: {proxy_url}")

        # OS-specific handling
        system = platform.system()
        options = ChromeOptions()

        if system == "Windows":
            print("It's Windows. Nothing to worry, thanks to Bill Gates.")
        elif system == "Linux":
            user_data_dir = tempfile.mkdtemp(prefix="udc_profile_")
            options.add_argument(f"--user-data-dir={user_data_dir}")
        else:
            raise RuntimeError(f"Unsupported OS: {system}")

        # Base Chrome flags
        options.add_argument("--log-level=3")
        options.add_argument("--no-sandbox")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument(f"user-agent={agent}")

        if headless:
            options.add_argument("--headless=new")

        # Selenium Wire proxy config
        seleniumwire_options = {
            "port": 8885,
            "verify_ssl": False,
            "proxy": {
                "http": proxy_url,
                "https": proxy_url,
                "no_proxy": "localhost,127.0.0.1"
            }
        }

        # Create the undetected_chromedriver with selenium-wire patched
        driver = Chrome(
            options=options,
            seleniumwire_options=seleniumwire_options,
            version_main=136,  # adjust to your local Chrome major version
            use_subprocess=True
        )

        return driver

    except Exception:
        traceback.print_exc()
        raise Exception("Failed to initialize undetected_chromedriver with proxy")


# def open_driver_with_proxy(headless: bool, agent: str, proxy_ip: str) -> webdriver.Chrome:
#     try:
#         # Parse proxy components
#         username, password, proxy_host, proxy_port = parse_proxy_url(proxy_ip)
#         proxy_url = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
#         print(f"Using Proxy: {proxy_url}")
#         system = platform.system()
#         # Chrome options setup
#         options = Options()
#         if system == "Windows":
#             print("Its Windows Nothing to Worry, Thanks to Bill Gates")
#             # options.add_argument(f"--user-data-dir=C:\\chrome_profiles\\profile_{profile_id}")
#         elif system == "Linux":
#             print("Added Profile in Linux")
#             # user_data_dir = tempfile.mkdtemp()
#             # options.add_argument(f"--user-data-dir=/tmp/udc_profile_{user_data_dir}")
#             user_data_dir = tempfile.mkdtemp(prefix="udc_profile_")
#             options.add_argument(f"--user-data-dir={user_data_dir}")
#         else:
#             raise RuntimeError(f"Unsupported OS: {system}")
#         options.add_argument('--log-level=3')
#         options.add_argument('ignore-certificate-errors')
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument(f'--user-data-dir=/tmp/chrome-data-{time.time()}')
#         options.add_argument('--disable-gpu')
#         options.add_argument('--disable-extensions')
#         options.add_argument('--disable-software-rasterizer')
#         options.add_argument('--start-maximized')
#         options.add_argument('--window-size=1920,1080')
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument(f"user-agent={agent}")
#         if headless:
#             options.add_argument('--headless')

#         # Proxy settings
#         seleniumwire_options = {
#         'port': 8885,
#         'verify_ssl': False,
#         'proxy': {
#             'http': proxy_url,
#             'https': proxy_url,
#             'no_proxy': 'localhost,127.0.0.1'
#             }
#             }

#         # Return configured driver
#         return webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options)
#     except:
#         traceback.print_exc()
#         raise Exception("Failed to initialize Chrome WebDriver with proxy")
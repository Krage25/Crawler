

def checkLogin(driver):
    try:
        print("Current URL:", driver.current_url)
        if "reddit.com" in driver.current_url and "login" not in driver.current_url:
            print("Login successful!")
        else:
            print("Login failed. Check your cookies.")
    except:
        pass
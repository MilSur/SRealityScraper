from selenium import webdriver

WEBDRIVER_EXECUTOR = 'http://selenium-hub:4444'

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

def get_webdriver():
    try:
        driver = webdriver.Remote(command_executor=WEBDRIVER_EXECUTOR, options=options)
        return driver
    except:
        return None
    

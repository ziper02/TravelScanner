import traceback


import platform
import selenium
from selenium.webdriver import Chrome, DesiredCapabilities
from selenium.webdriver.chrome.options import Options


'''Returns a Chrome Webdriver.'''

def prepare_driver_chrome(url,prof=None):
    options = Options()
    options.add_argument('-headless')
    options.add_argument("--lang=en-gb");
    options.add_argument('window-size=1920x1080')
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    if platform.system()=='Windows':
        driver = selenium.webdriver.Chrome(executable_path='C:\\Users\\Ziv\\PycharmProjects\\TravelScanner\\chromedriver.exe', options=options,desired_capabilities=caps)
    else:
        driver = selenium.webdriver.Chrome(
            executable_path='/usr/bin/chromedriver', options=options,
            desired_capabilities=caps)
    try:
        driver.get(url)
    except Exception:
        traceback.print_exc()
    driver.implicitly_wait(0)
    return driver


# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
#
#
# def prepare_driver_firefox(url):
#     options = Options()
#     options.headless = True
#     if platform.system() == 'Windows':
#         driver = webdriver.Firefox(options=options, executable_path=r'C:\\Users\\Ziv\\PycharmProjects\\TravelScanner\\geckodriver.exe')
#     try:
#         driver.get(url)
#     except Exception:
#         traceback.print_exc()
#     driver.implicitly_wait(0)
#     return driver
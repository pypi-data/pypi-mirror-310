import os
import time
import requests
import shutil
import logging
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

file_path = os.getcwd()
log_format = "%(asctime)s %(levelname)s %(message)s"
date_format = "%m-%d-%Y %H:%M:%S"
logging.basicConfig(filename=file_path+"/auto-metamask.log", level=logging.INFO,
                    format=log_format, datefmt=date_format)


def downloadMetamask(url):
    """Download the metamask extension

    :param url: Metamask extension download address (.zip)
    :type url: String
    :return: Extension file path
    :rtype: String
    """
    logging.info("Downloading metamask...")
    local_filename = file_path + '/' + url.split('/')[-1]

    if os.path.exists(local_filename):
        logging.info("Metamask " + local_filename + " found in cache")
        return local_filename

    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename


def setupWebdriver(metamask_path, chrome_path=None, version=None, chromedriver_path=None):
    """Initialize chrome browser and install metamask extension

    :param metamask_path: Extension file path
    :type metamask_path: String
    :param chrome_path: Chrome browser path, default is None.
    :type chrome_path: String
    :param version: Chrome browser version, make sure it matches the chromedriver version, if not provided, the latest version will be used, default is None. if chromedriver_path is provided, this parameter will be ignored.
    :type version: String
    :param chromedriver_path: Chromedriver file path, default is None.
    :type chromedriver_path: String
    :return: Selenium Chrome WebDriver
    :rtype: WebDriver
    """

    options = Options()
    # options.add_argument('--start-maximized')
    options.add_argument("--window-size=1440,900")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')

    # Chrome is controlled by automated test software
    # options.binary_location = "/Applications/Google Chrome Dev.app/Contents/MacOS/Google Chrome Dev"
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_extension(metamask_path)
    if chrome_path and version:
        if os.path.exists(chrome_path):
            options.binary_location = chrome_path
            logging.info("Chrome path is " + chrome_path + ", version is " + version)
        else:
            logging.warning("Chrome path not found")
    else:
        logging.warning("Chrome path or version not provided, using default")

    if chromedriver_path:
        s = Service(chromedriver_path)
    else:
        s = Service(ChromeDriverManager(version=version, path=chromedriver_path).install())
    global driver
    driver = webdriver.Chrome(service=s, options=options)

    # Selenium Stealth settings
    stealth(driver,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True,
            )

    global wait
    wait = WebDriverWait(driver, 20, 1)

    global wait_fast
    wait_fast = WebDriverWait(driver, 3, 1)

    global wait_slow
    wait_slow = WebDriverWait(driver, 40, 1)

    time.sleep(3)

    global metamask_handle
    metamask_handle = driver.window_handles[1]

    driver.switch_to.window(metamask_handle)
    time.sleep(2)

    global metamask_url
    metamask_url = driver.current_url.split('#')[0]

    return driver


def switchPage(func):
    @wraps(func)
    def switch(*args, **kwargs):
        current_handle = driver.current_window_handle
        driver.switch_to.window(metamask_handle)

        driver.get(metamask_url)

        try:
            wait_fast.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-testid='popover-close']"))).click()
        except Exception:
            logging.warning("No popover")

        func(*args, **kwargs)

        try:
            wait_fast.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-testid='popover-close']"))).click()
        except Exception:
            logging.warning("No popover")

        driver.switch_to.window(current_handle)
    return switch


@switchPage
def setupMetamask(recovery_phrase, password):
    """Setup metamask wallet

    :param recovery_phrase: Recovery phrase (12 words)
    :type recovery_phrase: String
    :param password: Wallet password (minimum 8 characters)
    :type password: String
    """

    wait_slow.until(EC.invisibility_of_element_located(
        (By.CSS_SELECTOR, "div[class='loading-overlay__container']")))
    time.sleep(1)

    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/ul/li[1]/div/input").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "    /html/body/div[1]/div/div[2]/div/div/div/ul/li[3]/button").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/button[1]").click()
    time.sleep(1)
    # Split the recovery phrase into individual words
    words = recovery_phrase.split(' ')
    word_count = len(words)

    # Check if the length of the words is valid
    if word_count not in [12, 15, 18, 21, 24]:
        logging.error(
            "Invalid recovery phrase. The phrase should be 12, 15, 18, 21, or 24 words long.")
    else:
        # Select the dropdown
        # //*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select
        # //*[contains(@class, 'dropdown__select')]
        # //div[@class='import-srp__container']//select[@class='dropdown__select']
        time.sleep(1)
        # For each input field
        for i in range(0, word_count):
            # Get the corresponding word
            word = words[i]

            # Input the word into the field
            input = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/div/div[3]/div[{i+1}]/div[1]/div/input")
            input.send_keys(word)

    # Click the confirm button
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button").click()

    # enter password
    input = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input")
    input.send_keys(password)
    input2 = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input")
    input2.send_keys(password)
    # checkbox
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[3]/label/span[1]/input").click()
    #create
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/button").click()
    # find the all done button and click
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[3]/button").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/button").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/button").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[1]/div/button/span").click()
    logging.info('Setup success')


@switchPage
def addNetwork(network_name, rpc_url, chain_id, currency_symbol):
    """Add a custom network

    :param network_name: Network name
    :type network_name: String
    :param rpc_url: RPC URL
    :type rpc_url: String
    :param chain_id: Chain ID
    :type chain_id: String
    :param currency_symbol: Currency symbol
    :type currency_symbol: String
    """

    # Switch to the settings page
    driver.get(metamask_url + '#settings/networks/add-network')
    #Name
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div[1]/div[1]/div/input").send_keys(network_name)
    #URL
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div[1]/div[2]/div").click()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div[1]/div[2]/div[2]/div/div/button").click()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div[1]/div[1]/div/input").send_keys(rpc_url)
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div[2]/button").click()

    #ChainId
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div[1]/div[3]/div/input").send_keys(chain_id)
    #Symbol
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div[1]/div[4]/div/input").send_keys(currency_symbol)
    #CONFIRM
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div[2]/button").click()


    logging.info('Add network success')


@switchPage
def changeNetwork(network_name):
    """Switch to a network

    :param network_name: Network name
    :type network_name: String
    """

    logging.info('Change network')


    # display the network list
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/button").click()
    # click the network name
    button = driver.find_element(By.XPATH, f"//div[@data-testid='{network_name}']")

    # Click the button
    button.click()
    logging.info('Change network success')


@switchPage
def importPK(priv_key):
    """Import private key

    :param priv_key: Private key
    :type priv_key: String
    """

    # Click the account menu
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/button").click()
    # Click the import account button
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div[2]/button").click()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div[2]/button").click()
    #input pk
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div/div[1]/div/input").send_keys(priv_key)
    #confirm
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/section/div/div/div[2]/button[2]").click()


    logging.info('Import PK success')


@switchPage
def connect():
    """Connect wallet
    """
    # connect
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/button[2]").click()
    time.sleep(3)
    #confirm
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/button[2]").click()

    logging.info('Connect wallet successfully')


@switchPage
def approve():
    """Approve wallet
    """

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'btn-primary')]"))).click()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'btn-primary')]"))).click()

    try:
        # This button is only available when the popup is closed
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='eth-overview-send']")))
    except Exception:
        logging.error("Approve failed")
        return

    logging.info('Approve successfully')


@switchPage
def approveTokens(cap=None):
    """Approve tokens

    :param cap: Spending limit, must be greater than 0, default is None.
    :type cap: Number
    """

    try:
        wait_fast.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Use default']")))
    except Exception:
        logging.warning('Refresh page')
        driver.refresh()

    if cap:
        if isinstance(cap, int) and cap > 0:
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[id='custom-spending-cap']"))).send_keys(str(cap))
        else:
            logging.error("Invalid cap")
            return
    else:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Use default']"))).click()

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='page-container-footer-next']"))).click()

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='page-container-footer-next']"))).click()

    try:
        # This button is only available when the popup is closed
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='eth-overview-send']")))
    except Exception:
        logging.error("Approve failed")
        return

    logging.info('Approve successfully')


@switchPage
def confirm():
    """Confirm wallet

    Use for Transaction, Sign, Deploy Contract, Create Token, Add Token, Sign In, etc.
    """

    try:
        wait_fast.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='page-container-footer-next']")))
    except Exception:
        logging.warning('Refresh page')
        driver.refresh()

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='page-container-footer-next']"))).click()

    try:
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='eth-overview-send']")))
    except Exception:
        logging.error("Connect wallet failed")
        return

    logging.info('Sign successfully')


@switchPage
def waitPending(timeout=40):
    """Wait pending

    :param timeout: Timeout (seconds)
    :type timeout: Number
    """

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "li[data-testid='home__activity-tab']"))).click()

    try:
        if timeout and isinstance(timeout, int):
            wait_temp = WebDriverWait(driver, timeout, 1)
        else:
            wait_temp = WebDriverWait(driver, 40, 1)

        wait_temp.until_not(EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, '.transaction-status-label--pending')))
    except Exception:
        logging.error("Wait pending failed or timeout")
        return

    logging.info('Wait pending successfully')

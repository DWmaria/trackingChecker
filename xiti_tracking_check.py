import json
from urllib.parse import urlparse
import argparse

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


parser = argparse.ArgumentParser()
parser.add_argument('--url', help='article url', required=True)
parser.add_argument('--chromedriver-path', help='chrome driver path (default: bin/chromedriver)', default='bin/chromedriver')
parser.add_argument('--collection-domain', help='SSL collection domain (default: logs1279)', default='logs1279')

args = parser.parse_args()

URL = args.url
DRIVER_PATH = args.chromedriver_path
SEARCH_TERM = args.collection_domain + '.xiti'



capabilities = DesiredCapabilities.CHROME
# capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

driver = webdriver.Chrome(
    DRIVER_PATH,
    desired_capabilities=capabilities,
)

def process_browser_logs_for_network_events(logs):
    """
    Return only relevant logs.
    """
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if ("Network.requestWillBeSent" in log["method"]
            and "Network.requestWillBeSentExtraInfo" not in log["method"]):
            if SEARCH_TERM in log["params"]["request"]["url"]:
                print("Noted the following xiti requests:")
                print(log["params"]["request"]["url"])
                yield log

def check_url(url):
    """
    Check the network log of a url, save a log file, and return the number of
    network requests containing 'xiti'
    """
    driver.get(url)
    logs = driver.get_log("performance")

    events = process_browser_logs_for_network_events(logs)
    count = len(list(events))

    return count

def main():
    check1 = True
    check2 = True

    # Step 1: Check for xiti requests in given url
    print("Check 1:")
    print("Checking", URL)

    count = check_url(URL)
    print("Number of xiti requests:", count)
    if count > 0 :
        print("SUCCESS!")
    else:
        check1 = False
        print("FAIL!")

    print("------------------------------")
    # Step 2: Check subdomain
    print("Check 2:")

    subdomain = 'http://' + urlparse(URL).netloc
    print("Checking", subdomain)

    count = check_url(subdomain)
    print("Number of xiti requests:", count)
    if not count > 0 :
        print("SUCCESS!")
    else:
        check2 = False
        print("FAIL!")

    print("=============================")

    print("Checks complete.")
    if not check1:
        print("Failed Check 1. URL produces no xiti requests.")
    if not check2:
        print("Failed Check 2. Subdomain produces xiti requests.")

    driver.quit()

if __name__ == '__main__':
    main()

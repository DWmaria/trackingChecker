# trackingChecker

Python script to check that xiti network requests are being sent by a URL and the subdomain.

## Setup
1. Install packages listed in requirements.txt
2. Place a relevant version of `chromedriver` in a directory called 'bin' inside the project directoy. You can find download links here: https://sites.google.com/chromium.org/driver/downloads

## Usage
```
usage: xiti_tracking_check.py [-h] --url URL [--chromedriver-path CHROMEDRIVER_PATH] [--collection-domain COLLECTION_DOMAIN]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             article url
  --chromedriver-path CHROMEDRIVER_PATH
                        chrome driver path (default: bin/chromedriver)
  --collection-domain COLLECTION_DOMAIN
                        SSL collection domain (default: logs1279)
```
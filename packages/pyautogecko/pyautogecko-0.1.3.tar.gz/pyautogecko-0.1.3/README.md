# pyautogecko
Fork of [geckodriver-autoinstaller](https://github.com/yeongbin-jo/python-geckodriver-autoinstaller) which is no longer mantained.
Automatically download and install [geckodriver](https://github.com/mozilla/geckodriver/releases/latest) that supports the currently installed version of firefox. This installer supports Linux, MacOS and Windows operating systems.

## Installation

```bash
pip install pyautogecko
```

## Usage
Just type `import pyautogecko` in the module you want to use geckodriver.

## Example
```
from selenium import webdriver
import pyautogecko


pyautogecko.install()  # Check if the current version of geckodriver exists
                                     # and if it doesn't exist, download it automatically,
                                     # then add geckodriver to path

driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
```

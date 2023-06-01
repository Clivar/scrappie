from dataclasses import dataclass
from typing import List, Dict, Any, Literal, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from shared_driver import SharedDriver

@dataclass
class Macro:
    kind: str
    xpath: Optional[str]
    extra: Optional[Any]

def validate_macros(macros: List[Macro]):
    known_kinds = {'scroll', 'click', 'wait', 'type'}
    for macro in macros:
        if macro.kind not in known_kinds:
            print(f"Unknown macro kind: {macro.kind}")
            return False
        if macro.kind == 'scroll' and (macro.xpath or macro.extra):
            print(f"Macro 'scroll' should not have 'xpath' or 'extra' properties")
            return False
        if macro.kind == 'click' and (not macro.xpath or macro.extra):
            print(f"Macro 'click' should have 'xpath' and should not have 'extra'")
            return False
        if macro.kind == 'wait' and not (macro.xpath or (macro.extra and isinstance(macro.extra, int))):
            print(f"Macro 'wait' should have 'xpath' or 'extra' (as int)")
            return False
        if macro.kind == 'type' and (not macro.xpath or not macro.extra):
            print(f"Macro 'type' should have both 'xpath' and 'extra'")
            return False
    return True

def perform_macro(macro: Macro):
    driver = SharedDriver.get_instance()
    if macro.kind == 'scroll':
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait a little for potential JavaScript loading after scroll

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # No more new data loaded
                break
            last_height = new_height
    elif macro.kind == 'click':
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, macro['xpath'])))
        element.click()
    elif macro.kind == 'wait':
        if macro.get('xpath'):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, macro['xpath'])))
        else:
            time.sleep(macro['extra'])
    elif macro.kind == 'type':
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, macro['xpath'])))
        element.send_keys(macro['extra'])

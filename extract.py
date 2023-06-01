from typing import List
from jsonpath_ng import parse
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from capture import capture_element, capture_json_value

from common import retry
from macro import Macro, perform_macro
from shared_driver import SharedDriver

@retry()
def extract_json(url: str, path: str, capture_type: str):
    response = requests.get(url, timeout=5).json()
    jsonpath_expr = parse(path)
    values = [match.value for match in jsonpath_expr.find(response)]
    for i, value in values:
        match_key, match = capture_json_value(match, capture_type, url)
        yield {
            'order': i,
            'match_key': match_key,
            'match': match
        }

@retry()
def extract_html(url: str, path: str, macros: List[Macro], capture_type: str):
    driver = SharedDriver.get_instance()    
    driver.get(url)

    for macro in macros:
        perform_macro(macro)

    # Wait up to 10 seconds for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))

    elements = driver.find_elements(By.XPATH, path)

    for i, element in elements:
        match_key, match = capture_element(element, capture_type, url)
        yield {
            'order': i,
            'match_key': match_key,
            'match': match
        }
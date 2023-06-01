from typing import Any, List
from jsonpath_ng import parse
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from capture import capture_element, capture_json_value

from common import retry
from macro import Macro, perform_macro
from shared_driver import SharedDriver
from dataclasses import dataclass

@dataclass
class ExtractResult:
    order: int
    match_key: Any
    match: Any


@retry()
def extract_json(url: str, post_body: str, path: str, capture_type: str):
    if post_body:
        headers = {"Content-Type": "application/json", 'Accept': 'application/json'}
        response = requests.post(url, data=post_body, headers=headers, timeout=5).json()
    else:
        response = requests.get(url, timeout=5).json()
    jsonpath_expr = parse(path)
    values = [match.value for match in jsonpath_expr.find(response)]
    for i, value in enumerate(values):
        match_key, match = capture_json_value(value, capture_type, url)
        yield ExtractResult(i, match_key, match)

@retry()
def extract_html(url: str, path: str, macros: List[Macro], capture_type: str):
    driver = SharedDriver.get_instance()    
    driver.get(url)

    for macro in macros:
        perform_macro(macro)

    # Wait up to 10 seconds for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))

    elements = driver.find_elements(By.XPATH, path)

    for i, element in enumerate(elements):
        match_key, match = capture_element(element, capture_type, url)
        yield ExtractResult(i, match_key, match)
